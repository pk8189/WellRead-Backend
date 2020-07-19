from datetime import datetime
from typing import Any, List

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class NoteBase(BaseModel):
    id: int
    create_date: datetime
    content: str
    slack_user_id: str
    slack_club_id: int
    slack_user: Any
    slack_club: Any
    tags: List[Any]


class NoteCreate(BaseModel):
    content: str
    slack_user_id: str
    slack_club_id: int


class NoteUpdate(BaseModel):
    content: str


class NoteAddTags(BaseModel):
    tags: List[int]


class NoteDelete(BaseModel):
    id: int


class Note(NoteBase):
    class Config:
        orm_mode = True
