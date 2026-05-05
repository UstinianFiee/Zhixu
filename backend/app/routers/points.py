from datetime import date
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select, func
from app.database import get_session
from app.models import User, PointTransaction, CheckIn
from app.schemas import PointsResponse, PointTransactionResponse, PointsHistoryResponse
from app.deps import get_current_user
from app.services.points_service import get_level_info, award_points

router = APIRouter()


@router.get("/points/me", response_model=PointsResponse)
def get_my_points(
    current_user: User = Depends(get_current_user),
):
    level, title, next_points = get_level_info(current_user.total_points)
    return PointsResponse(
        total_points=current_user.total_points,
        current_level=level,
        level_title=title,
        next_level_points=next_points,
    )


@router.get("/points/history", response_model=PointsHistoryResponse)
def get_points_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    offset = (page - 1) * limit
    total = db.exec(
        select(func.count()).select_from(PointTransaction)
        .where(PointTransaction.user_id == current_user.id)
    ).first() or 0
    items = db.exec(
        select(PointTransaction)
        .where(PointTransaction.user_id == current_user.id)
        .order_by(PointTransaction.created_at.desc())
        .offset(offset)
        .limit(limit)
    ).all()
    return PointsHistoryResponse(
        items=[PointTransactionResponse.model_validate(i) for i in items],
        total=total,
    )


@router.get("/points/rank/me")
def get_my_points_rank(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    rank = db.exec(
        select(func.count()).select_from(User)
        .where(User.total_points > current_user.total_points)
    ).first() or 0
    return {"rank": rank + 1, "total_points": current_user.total_points}


@router.post("/checkin")
def do_checkin(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    """每日打卡"""
    today = date.today()
    existing = db.exec(
        select(CheckIn).where(
            CheckIn.user_id == current_user.id,
            CheckIn.date == today,
        )
    ).first()
    if existing:
        return {"message": "今日已打卡", "checked_in": True, "streak_days": existing.streak_days}

    # 计算连续天数
    from datetime import timedelta
    yesterday = today - timedelta(days=1)
    prev = db.exec(
        select(CheckIn).where(
            CheckIn.user_id == current_user.id,
            CheckIn.date == yesterday,
        )
    ).first()
    streak = (prev.streak_days + 1) if prev else 1

    # 积分：基础+3，连续7天+30
    points = 3
    if streak >= 7 and streak % 7 == 0:
        points += 30

    record = CheckIn(
        user_id=current_user.id,
        date=today,
        streak_days=streak,
        points_earned=points,
    )
    db.add(record)
    award_points(db, current_user.id, points, "daily_checkin")
    db.commit()
    return {"message": f"打卡成功 +{points}积分", "checked_in": True, "streak_days": streak, "points_earned": points}


@router.get("/checkin/status")
def checkin_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    """获取今日打卡状态和连续天数"""
    today = date.today()
    existing = db.exec(
        select(CheckIn).where(
            CheckIn.user_id == current_user.id,
            CheckIn.date == today,
        )
    ).first()
    latest = db.exec(
        select(CheckIn)
        .where(CheckIn.user_id == current_user.id)
        .order_by(CheckIn.date.desc())
        .limit(1)
    ).first()
    return {
        "checked_in_today": existing is not None,
        "streak_days": latest.streak_days if latest else 0,
    }


@router.get("/checkin/month")
def checkin_month(
    year: int = Query(...),
    month: int = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    """获取某月打卡日期列表"""
    from datetime import timedelta
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)
    records = db.exec(
        select(CheckIn).where(
            CheckIn.user_id == current_user.id,
            CheckIn.date >= start,
            CheckIn.date < end,
        )
    ).all()
    dates = [r.date.isoformat() for r in records if r.date]
    return {"dates": dates}
