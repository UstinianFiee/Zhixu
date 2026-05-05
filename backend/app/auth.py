from datetime import datetime, timedelta, timezone
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from sqlmodel import Session, select
from app.config import settings
from app.database import get_session
from app.models import User, PointTransaction
from app.schemas import UserRegister, UserLogin, TokenResponse, UserResponse, ProfileUpdate
from app.deps import get_current_user

router = APIRouter()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def _user_response(user: User) -> UserResponse:
    return UserResponse.model_validate(user)


@router.post("/register", response_model=TokenResponse)
def register(data: UserRegister, db: Session = Depends(get_session)):
    existing = db.exec(select(User).where(
        (User.email == data.email) | (User.username == data.username)
    )).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名或邮箱已存在")

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        total_points=50,
        current_level=1,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    pt = PointTransaction(user_id=user.id, points_change=50, reason="new_user_register")
    db.add(pt)
    db.commit()

    token_data = {"sub": str(user.id)}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
        user=_user_response(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.email == data.email)).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="邮箱或密码错误")

    user.last_login_at = datetime.now(timezone.utc)
    db.add(user)
    db.commit()
    db.refresh(user)

    token_data = {"sub": str(user.id)}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
        user=_user_response(user),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(current_user: User = Depends(get_current_user)):
    token_data = {"sub": str(current_user.id)}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
        user=_user_response(current_user),
    )


@router.post("/logout")
def logout():
    return {"message": "已登出"}


@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return _user_response(current_user)


@router.put("/profile", response_model=UserResponse)
def update_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    user = db.get(User, current_user.id)
    if data.nickname is not None:
        user.nickname = data.nickname.strip()[:50] if data.nickname.strip() else None
    if data.avatar_url is not None:
        user.avatar_url = data.avatar_url if data.avatar_url else None
    db.add(user)
    db.commit()
    db.refresh(user)
    return _user_response(user)
