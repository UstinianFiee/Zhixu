from typing import Optional
from datetime import datetime, date as date_type
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Date, DateTime, Text, func


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=50)
    nickname: Optional[str] = Field(default=None, max_length=50)
    email: str = Field(unique=True, index=True, max_length=100)
    password_hash: str = Field(max_length=255)
    total_points: int = Field(default=0, index=True)
    current_level: int = Field(default=1)
    is_admin: bool = Field(default=False)
    created_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime, default=func.now()))
    last_login_at: Optional[datetime] = None
    avatar_url: Optional[str] = Field(default=None, sa_column=Column(Text))


class UserLearningRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    word_id: str = Field(max_length=50)
    word: str = Field(max_length=100, index=True)
    is_correct: bool
    time_spent_ms: int
    speed_wpm: int
    created_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime, default=func.now(), index=True))


class PointTransaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    points_change: int
    reason: str = Field(max_length=255)
    created_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime, default=func.now(), index=True))


class DailyContent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: Optional[date_type] = Field(default=None, sa_column=Column(Date, index=True))
    type: str = Field(max_length=20)  # quote | song | article
    title: str = Field(max_length=200)
    content: str = Field(sa_column=Column(Text))
    author: Optional[str] = None
    source_url: Optional[str] = None
    cover_url: Optional[str] = None


class WordList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    word_count: int = Field(default=0)
    is_preset: bool = Field(default=True)
    created_by: Optional[int] = None


class Word(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    wordlist_id: int = Field(foreign_key="wordlist.id", index=True)
    word: str = Field(max_length=100, index=True)
    translation: str = Field(max_length=255)
    phonetic: Optional[str] = None
    example_sentence: Optional[str] = Field(default=None, sa_column=Column(Text))


class Favorite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    content_type: str = Field(max_length=20)  # quote | song | article
    content_id: int = Field(index=True)
    created_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime, default=func.now()))


class CheckIn(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    date: Optional[date_type] = Field(default=None, sa_column=Column(Date, index=True))
    streak_days: int = Field(default=1)
    points_earned: int = Field(default=0)
