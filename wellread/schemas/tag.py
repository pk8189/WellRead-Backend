from datetime import datetime
from typing import Any

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class TagBase(BaseModel):
    id: int
    name: str
    create_date: datetime
    slack_club_id: int
    slack_club: Any
    notes: list


class TagCreate(BaseModel):
    name: str
    slack_club_id: int


class TagUpdate(BaseModel):
    name: str


class TagDelete(BaseModel):
    id: int


class Tag(TagBase):
    class Config:
        orm_mode = True
