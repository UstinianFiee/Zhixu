from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from app.database import get_session
from app.models import User
from app.schemas import LeaderboardResponse
from app.deps import get_current_user
from app.services import leaderboard_service as lbs

router = APIRouter()

VALID_TYPES = ["total", "month", "week", "daily", "speed", "mistake"]


@router.get("/leaderboard/{board_type}", response_model=LeaderboardResponse)
def get_leaderboard(
    board_type: str,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    if board_type == "total":
        entries, _ = lbs.get_total_leaderboard(db, page, limit)
    elif board_type == "month":
        entries = lbs.get_period_leaderboard(db, "month", page, limit)
    elif board_type == "week":
        entries = lbs.get_period_leaderboard(db, "week", page, limit)
    elif board_type == "daily":
        entries = lbs.get_daily_star_leaderboard(db, page, limit)
    elif board_type == "speed":
        entries = lbs.get_speed_leaderboard(db, page, limit)
    elif board_type == "mistake":
        entries = lbs.get_mistake_leaderboard(db, page, limit)
    else:
        entries = []

    my_rank = lbs.get_user_rank(db, current_user.id, board_type)
    return LeaderboardResponse(type=board_type, entries=entries, my_rank=my_rank)


@router.get("/leaderboard/{board_type}/{user_id}/rank")
def get_user_rank(
    board_type: str,
    user_id: int,
    db: Session = Depends(get_session),
):
    rank = lbs.get_user_rank(db, user_id, board_type)
    return {"user_id": user_id, "type": board_type, "rank": rank}
