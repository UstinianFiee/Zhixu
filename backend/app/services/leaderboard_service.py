from datetime import datetime, timedelta, date
from typing import List, Optional
from sqlmodel import Session, select, func, col
from app.models import User, UserLearningRecord, PointTransaction
from app.schemas import LeaderboardEntry


def get_total_leaderboard(db: Session, page: int = 1, limit: int = 20) -> tuple[List[LeaderboardEntry], Optional[int]]:
    offset = (page - 1) * limit
    results = db.exec(
        select(User.id, User.username, User.nickname, User.avatar_url, User.total_points)
        .order_by(User.total_points.desc())
        .offset(offset)
        .limit(limit)
    ).all()
    entries = [
        LeaderboardEntry(rank=offset + i + 1, user_id=r[0], username=r[1], nickname=r[2], avatar_url=r[3], score=r[4])
        for i, r in enumerate(results)
    ]
    return entries, None


def get_period_leaderboard(db: Session, period: str, page: int = 1, limit: int = 20) -> List[LeaderboardEntry]:
    now = datetime.utcnow()
    if period == "month":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif period == "week":
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    else:  # daily
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    offset = (page - 1) * limit
    subq = (
        select(
            PointTransaction.user_id,
            func.sum(PointTransaction.points_change).label("score")
        )
        .where(PointTransaction.created_at >= start)
        .group_by(PointTransaction.user_id)
        .subquery()
    )
    results = db.exec(
        select(User.id, User.username, User.nickname, User.avatar_url, subq.c.score)
        .join(subq, User.id == subq.c.user_id)
        .order_by(subq.c.score.desc())
        .offset(offset)
        .limit(limit)
    ).all()
    return [
        LeaderboardEntry(rank=offset + i + 1, user_id=r[0], username=r[1], nickname=r[2], avatar_url=r[3], score=int(r[4] or 0))
        for i, r in enumerate(results)
    ]


def get_daily_star_leaderboard(db: Session, page: int = 1, limit: int = 20) -> List[LeaderboardEntry]:
    """今日学习星榜: 正确单词数"""
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    offset = (page - 1) * limit
    subq = (
        select(
            UserLearningRecord.user_id,
            func.count().filter(UserLearningRecord.is_correct == True).label("correct_count")
        )
        .where(UserLearningRecord.created_at >= today)
        .group_by(UserLearningRecord.user_id)
        .subquery()
    )
    results = db.exec(
        select(User.id, User.username, User.nickname, User.avatar_url, subq.c.correct_count)
        .join(subq, User.id == subq.c.user_id)
        .order_by(subq.c.correct_count.desc())
        .offset(offset)
        .limit(limit)
    ).all()
    return [
        LeaderboardEntry(rank=offset + i + 1, user_id=r[0], username=r[1], nickname=r[2], avatar_url=r[3], score=int(r[4] or 0))
        for i, r in enumerate(results)
    ]


def get_speed_leaderboard(db: Session, page: int = 1, limit: int = 20) -> List[LeaderboardEntry]:
    """速度之王榜: 近7天平均打字速度"""
    week_ago = datetime.utcnow() - timedelta(days=7)
    offset = (page - 1) * limit
    subq = (
        select(
            UserLearningRecord.user_id,
            func.avg(UserLearningRecord.speed_wpm).label("avg_speed")
        )
        .where(
            UserLearningRecord.created_at >= week_ago,
            UserLearningRecord.is_correct == True,
        )
        .group_by(UserLearningRecord.user_id)
        .subquery()
    )
    results = db.exec(
        select(User.id, User.username, User.nickname, User.avatar_url, subq.c.avg_speed)
        .join(subq, User.id == subq.c.user_id)
        .order_by(subq.c.avg_speed.desc())
        .offset(offset)
        .limit(limit)
    ).all()
    return [
        LeaderboardEntry(rank=offset + i + 1, user_id=r[0], username=r[1], nickname=r[2], avatar_url=r[3], score=int(r[4] or 0))
        for i, r in enumerate(results)
    ]


def get_mistake_leaderboard(db: Session, page: int = 1, limit: int = 20) -> List[LeaderboardEntry]:
    """错题攻克榜: 近7天攻克错题数（之前错后来对）"""
    week_ago = datetime.utcnow() - timedelta(days=7)
    offset = (page - 1) * limit
    subq = (
        select(
            UserLearningRecord.user_id,
            func.count().filter(UserLearningRecord.is_correct == False).label("wrong_count")
        )
        .where(UserLearningRecord.created_at >= week_ago)
        .group_by(UserLearningRecord.user_id)
        .subquery()
    )
    results = db.exec(
        select(User.id, User.username, User.nickname, User.avatar_url, subq.c.wrong_count)
        .join(subq, User.id == subq.c.user_id)
        .order_by(subq.c.wrong_count.desc())
        .offset(offset)
        .limit(limit)
    ).all()
    return [
        LeaderboardEntry(rank=offset + i + 1, user_id=r[0], username=r[1], nickname=r[2], avatar_url=r[3], score=int(r[4] or 0))
        for i, r in enumerate(results)
    ]


def get_user_rank(db: Session, user_id: int, board_type: str) -> Optional[int]:
    """获取用户在指定排行榜的排名"""
    if board_type == "total":
        sub = select(User.total_points).where(User.id == user_id).scalar_subquery()
        rank = db.exec(
            select(func.count()).where(User.total_points > sub)
        ).first()
        return (rank or 0) + 1
    return None
