import random
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from app.database import get_session
from app.models import WordList, Word, UserLearningRecord, User
from app.schemas import (
    WordListResponse, WordResponse, PracticeRequest, CheckRequest,
    CheckResponse, SessionCompleteRequest, SessionCompleteResponse,
)
from app.deps import get_current_user
from app.services.points_service import award_points, get_level_info

router = APIRouter()


@router.get("/wordlists", response_model=list[WordListResponse])
def get_wordlists(db: Session = Depends(get_session)):
    wordlists = db.exec(select(WordList).order_by(WordList.id)).all()
    return [WordListResponse.model_validate(wl) for wl in wordlists]


@router.get("/wordlists/{wordlist_id}/words", response_model=list[WordResponse])
def get_words(
    wordlist_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_session),
):
    offset = (page - 1) * limit
    words = db.exec(
        select(Word)
        .where(Word.wordlist_id == wordlist_id)
        .offset(offset)
        .limit(limit)
    ).all()
    return [WordResponse.model_validate(w) for w in words]


@router.get("/wordlists/{wordlist_id}/count")
def get_word_count(wordlist_id: int, db: Session = Depends(get_session)):
    count = db.exec(
        select(func.count()).select_from(Word).where(Word.wordlist_id == wordlist_id)
    ).first()
    return {"wordlist_id": wordlist_id, "count": count or 0}


@router.post("/words/practice", response_model=WordResponse)
def get_practice_word(req: PracticeRequest, db: Session = Depends(get_session)):
    count = db.exec(
        select(func.count()).select_from(Word).where(Word.wordlist_id == req.wordlist_id)
    ).first()
    if not count or count == 0:
        raise HTTPException(status_code=404, detail="词库中没有单词")

    offset = random.randint(0, count - 1)
    word = db.exec(
        select(Word)
        .where(Word.wordlist_id == req.wordlist_id)
        .offset(offset)
        .limit(1)
    ).first()
    if not word:
        raise HTTPException(status_code=404, detail="无法获取单词")
    return WordResponse.model_validate(word)


@router.post("/words/check", response_model=CheckResponse)
def check_word(
    req: CheckRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    is_correct = req.user_input.strip().lower() == req.word.strip().lower()
    speed_wpm = int(60000 / req.time_spent_ms) if req.time_spent_ms > 0 else 0

    record = UserLearningRecord(
        user_id=current_user.id,
        word_id=req.word,
        word=req.word,
        is_correct=is_correct,
        time_spent_ms=req.time_spent_ms,
        speed_wpm=speed_wpm,
    )
    db.add(record)

    points_earned = 0
    streak = 0
    if is_correct:
        points_earned = 2

        # 检查连续正确
        recent = db.exec(
            select(UserLearningRecord)
            .where(UserLearningRecord.user_id == current_user.id)
            .order_by(UserLearningRecord.created_at.desc())
            .limit(10)
        ).all()
        streak = 1
        for r in recent:
            if r.is_correct:
                streak += 1
            else:
                break
        if streak >= 10 and streak % 10 == 1:
            points_earned += 5  # 连续正确奖励

        award_points(db, current_user.id, points_earned, "word_practice")

    db.commit()
    return CheckResponse(
        is_correct=is_correct,
        correct_word=req.word,
        speed_wpm=speed_wpm,
        points_earned=points_earned,
        streak=streak,
    )


@router.post("/sessions/complete", response_model=SessionCompleteResponse)
def complete_session(
    req: SessionCompleteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    points_earned = 0
    if req.stats.total >= 10:
        points_earned = 3
        award_points(db, current_user.id, points_earned, "session_complete")

    user = db.get(User, current_user.id)
    level, title, _ = get_level_info(user.total_points)
    return SessionCompleteResponse(
        points_earned=points_earned,
        total_points=user.total_points,
        current_level=level,
        level_title=title,
    )


@router.get("/words/errors")
def get_error_book(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    """错题本：获取用户所有错误单词及错误次数"""
    subq = (
        select(
            UserLearningRecord.word,
            func.count().label("error_count"),
            func.max(UserLearningRecord.created_at).label("last_attempt"),
        )
        .where(
            UserLearningRecord.user_id == current_user.id,
            UserLearningRecord.is_correct == False,
        )
        .group_by(UserLearningRecord.word)
        .order_by(func.count().desc())
        .subquery()
    )
    results = db.exec(subq).all()
    items = []
    for row in results:
        # Try to get translation from Word table
        word_entry = db.exec(
            select(Word).where(Word.word == row[0]).limit(1)
        ).first()
        items.append({
            "word": row[0],
            "translation": word_entry.translation if word_entry else "",
            "phonetic": word_entry.phonetic if word_entry else "",
            "error_count": row[1],
            "last_attempt": row[2].isoformat() if row[2] else "",
        })
    return items


@router.get("/words/dashboard")
def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    """学习看板数据"""
    total_records = db.exec(
        select(func.count()).select_from(UserLearningRecord)
        .where(UserLearningRecord.user_id == current_user.id)
    ).first() or 0
    correct_count = db.exec(
        select(func.count()).select_from(UserLearningRecord)
        .where(
            UserLearningRecord.user_id == current_user.id,
            UserLearningRecord.is_correct == True,
        )
    ).first() or 0
    wrong_count = total_records - correct_count
    avg_speed = db.exec(
        select(func.avg(UserLearningRecord.speed_wpm))
        .where(
            UserLearningRecord.user_id == current_user.id,
            UserLearningRecord.is_correct == True,
        )
    ).first() or 0
    # Today stats
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    today_correct = db.exec(
        select(func.count()).select_from(UserLearningRecord)
        .where(
            UserLearningRecord.user_id == current_user.id,
            UserLearningRecord.is_correct == True,
            UserLearningRecord.created_at >= today,
        )
    ).first() or 0
    return {
        "total_records": total_records,
        "correct_count": correct_count,
        "wrong_count": wrong_count,
        "avg_speed": int(avg_speed),
        "today_correct": today_correct,
        "total_points": current_user.total_points,
        "current_level": current_user.current_level,
    }
