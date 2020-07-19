from datetime import datetime

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from wellread.schemas.club import Club
from wellread.schemas.user import User


class NoteBase(BaseModel):
    id: int
    create_date: datetime
    content: str
    slack_user_id: str
    slack_club_id: int
    slack_user: User
    slack_club: Club


class NoteCreate(BaseModel):
    content: str
    slack_user_id: str
    slack_club_id: int


class NoteUpdate(BaseModel):
    content: str


class NoteDelete(BaseModel):
    id: int


class Note(NoteBase):
    class Config:
        orm_mode = True
