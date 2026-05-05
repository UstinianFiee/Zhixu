from sqlmodel import Session, select
from app.models import User, PointTransaction

# 等级体系: (所需积分, 等级, 称号)
LEVEL_THRESHOLDS = [
    (0, 1, "文艺学徒"),
    (200, 2, "单词小生"),
    (500, 3, "笔墨行者"),
    (1000, 4, "浮光阅者"),
    (2000, 5, "英文探路者"),
    (3500, 6, "星夜记忆者"),
    (5500, 7, "轻文艺学士"),
    (8000, 8, "键盘诗人"),
    (12000, 9, "安宁守护者"),
    (18000, 10, "独行大师"),
]


def get_level_info(points: int) -> tuple[int, str, int]:
    """根据积分返回 (等级, 称号, 下一级所需积分)"""
    current_level = 1
    current_title = "文艺学徒"
    next_points = 200

    for threshold, level, title in LEVEL_THRESHOLDS:
        if points >= threshold:
            current_level = level
            current_title = title
        else:
            next_points = threshold
            break
    else:
        next_points = -1  # 已满级

    return current_level, current_title, next_points


def award_points(db: Session, user_id: int, amount: int, reason: str) -> User:
    """为用户增加积分并更新等级"""
    user = db.get(User, user_id)
    if not user:
        return None

    pt = PointTransaction(user_id=user_id, points_change=amount, reason=reason)
    db.add(pt)

    user.total_points += amount
    new_level, _, _ = get_level_info(user.total_points)
    user.current_level = new_level
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
