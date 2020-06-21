from datetime import datetime
from typing import List

from pydantic import BaseModel


class Workspace(BaseModel):
    created: datetime

    class Config:
        orm_mode = True


class Club(BaseModel):
    workspace: Workspace


class User(BaseModel):
    email: str
    clubs: List[Club]

    class Config:
        orm_mode = True


class Tag(BaseModel):
    _id: str
    name: str
    club: Club
    created_by: User

    class Config:
        orm_mode = True


class Note(BaseModel):
    _id: str
    ts: datetime
    club: Club
    tags: List[Tag]
    created_by: User

    class Config:
        orm_mode = True
