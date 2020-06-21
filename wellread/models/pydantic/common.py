from datetime import datetime
from typing import List

from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str = None

    class Config:
        orm_mode = True


class Tag(BaseModel):
    name: str
    club_id: str
    created_by: User

    class Config:
        orm_mode = True


class Note(BaseModel):
    ts: datetime
    club_id: str
    tags: List[Tag]
    created_by: User

    class Config:
        orm_mode = True
