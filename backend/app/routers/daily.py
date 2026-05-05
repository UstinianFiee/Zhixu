from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import DailyContent, User, Favorite
from app.schemas import DailyContentResponse, DailyContentCreate, FavoriteResponse
from app.deps import get_current_user, get_optional_user
from app.services.points_service import award_points

router = APIRouter()


def _get_daily_content(db: Session, content_type: str) -> DailyContentResponse:
    today = date.today()
    content = db.exec(
        select(DailyContent)
        .where(DailyContent.type == content_type, DailyContent.date == today)
    ).first()
    if not content:
        content = db.exec(
            select(DailyContent)
            .where(DailyContent.type == content_type)
            .order_by(DailyContent.date.desc())
        ).first()
    if not content:
        raise HTTPException(status_code=404, detail=f"暂无{content_type}内容")
    return DailyContentResponse.model_validate(content)


@router.get("/daily/quote", response_model=DailyContentResponse)
def get_daily_quote(db: Session = Depends(get_session)):
    return _get_daily_content(db, "quote")


@router.get("/daily/song", response_model=DailyContentResponse)
def get_daily_song(db: Session = Depends(get_session)):
    return _get_daily_content(db, "song")


@router.get("/daily/article", response_model=DailyContentResponse)
def get_daily_article(db: Session = Depends(get_session)):
    return _get_daily_content(db, "article")


@router.post("/content/{content_type}/{content_id}/favorite")
def favorite_content(
    content_type: str,
    content_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    content = db.get(DailyContent, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="内容不存在")

    existing = db.exec(
        select(Favorite).where(
            Favorite.user_id == current_user.id,
            Favorite.content_type == content_type,
            Favorite.content_id == content_id,
        )
    ).first()
    if existing:
        db.delete(existing)
        db.commit()
        return {"message": "已取消收藏", "favorited": False}

    fav = Favorite(
        user_id=current_user.id,
        content_type=content_type,
        content_id=content_id,
    )
    db.add(fav)
    award_points(db, current_user.id, 1, "favorite_content")
    db.commit()
    return {"message": "收藏成功 +1积分", "favorited": True}


@router.get("/favorites/check/{content_type}/{content_id}")
def check_favorite(
    content_type: str,
    content_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    existing = db.exec(
        select(Favorite).where(
            Favorite.user_id == current_user.id,
            Favorite.content_type == content_type,
            Favorite.content_id == content_id,
        )
    ).first()
    return {"favorited": existing is not None}


@router.get("/favorites")
def get_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    """获取用户收藏列表（含内容详情）"""
    favorites = db.exec(
        select(Favorite)
        .where(Favorite.user_id == current_user.id)
        .order_by(Favorite.created_at.desc())
    ).all()
    items = []
    for fav in favorites:
        content = db.get(DailyContent, fav.content_id)
        items.append({
            "id": fav.id,
            "content_type": fav.content_type,
            "content_id": fav.content_id,
            "created_at": fav.created_at.isoformat() if fav.created_at else "",
            "title": content.title if content else "已删除",
            "content": content.content if content else "",
            "author": content.author if content else None,
        })
    return items
