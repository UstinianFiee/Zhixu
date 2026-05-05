from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel


# ── Auth ──
class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    nickname: Optional[str] = None
    email: str
    total_points: int
    current_level: int
    is_admin: bool
    created_at: datetime
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


# ── Daily Content ──
class DailyContentResponse(BaseModel):
    id: int
    date: date
    type: str
    title: str
    content: str
    author: Optional[str] = None
    source_url: Optional[str] = None
    cover_url: Optional[str] = None

    class Config:
        from_attributes = True


class DailyContentCreate(BaseModel):
    date: date
    type: str
    title: str
    content: str
    author: Optional[str] = None
    source_url: Optional[str] = None
    cover_url: Optional[str] = None


# ── Words ──
class WordListResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    word_count: int
    is_preset: bool

    class Config:
        from_attributes = True


class WordResponse(BaseModel):
    id: int
    word: str
    translation: str
    phonetic: Optional[str] = None
    example_sentence: Optional[str] = None

    class Config:
        from_attributes = True


class PracticeRequest(BaseModel):
    wordlist_id: int
    session_id: str


class CheckRequest(BaseModel):
    word: str
    user_input: str
    time_spent_ms: int
    session_id: Optional[str] = None


class CheckResponse(BaseModel):
    is_correct: bool
    correct_word: str
    speed_wpm: int
    points_earned: int = 0
    streak: int = 0


class SessionStats(BaseModel):
    total: int = 0
    correct: int = 0
    wrong: int = 0
    avg_speed: int = 0
    duration_ms: int = 0


class SessionCompleteRequest(BaseModel):
    session_id: str
    stats: SessionStats


class SessionCompleteResponse(BaseModel):
    points_earned: int
    total_points: int
    current_level: int
    level_title: str


# ── Leaderboard ──
class LeaderboardEntry(BaseModel):
    rank: int
    user_id: int
    username: str
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    score: int


class LeaderboardResponse(BaseModel):
    type: str
    entries: List[LeaderboardEntry]
    my_rank: Optional[int] = None


# ── Points ──
class PointsResponse(BaseModel):
    total_points: int
    current_level: int
    level_title: str
    next_level_points: int


class PointTransactionResponse(BaseModel):
    id: int
    points_change: int
    reason: str
    created_at: datetime

    class Config:
        from_attributes = True


class PointsHistoryResponse(BaseModel):
    items: List[PointTransactionResponse]
    total: int


# ── Admin ──
class WordListCreate(BaseModel):
    name: str
    description: Optional[str] = None


class WordImport(BaseModel):
    word: str
    translation: str
    phonetic: Optional[str] = None
    example_sentence: Optional[str] = None


class WordImportBatch(BaseModel):
    words: List[WordImport]


class ErrorBookEntry(BaseModel):
    word: str
    translation: str
    phonetic: Optional[str] = None
    error_count: int
    last_attempt: datetime


class FavoriteResponse(BaseModel):
    id: int
    content_type: str
    content_id: int
    created_at: datetime
    title: str
    content: str
    author: Optional[str] = None
