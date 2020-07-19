from datetime import datetime
from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class ClubBase(BaseModel):
    id: int
    book_title: str
    channel_id: str
    create_date: datetime
    is_active: bool
    admin_user_id: str
    slack_users: list
    tags: list
    next_meeting: Optional[datetime] = None


class ClubCreate(BaseModel):
    book_title: str
    channel_id: str
    admin_user_id: str
    next_meeting: Optional[datetime] = None


class ClubUpdate(BaseModel):
    book_title: Optional[str] = None
    channel_id: Optional[str] = None
    is_active: Optional[bool] = None
    next_meeting: Optional[datetime] = None


class ClubDelete(BaseModel):
    id: str


class Club(ClubBase):
    class Config:
        orm_mode = True
