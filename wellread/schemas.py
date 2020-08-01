from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


# Base models which map to the sqlalchemy ORM
class TeamBase(BaseModel):
    team_id: str
    name: Optional[str] = None
    domain: Optional[str] = None
    email_domain: Optional[str] = None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    slack_id_team_id: str
    name: str
    tz: str
    locale: str
    team_id: str

    class Config:
        orm_mode = True


class ClubBase(BaseModel):
    id: int
    book_title: str
    channel_id: str
    create_date: datetime
    is_active: bool
    admin_user_id: str
    intro_message_ts: Optional[str] = None

    class Config:
        orm_mode = True


class NoteBase(BaseModel):
    id: int
    create_date: datetime
    content: str
    slack_user_id: str
    slack_club_id: int
    private: bool

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    id: int
    name: str
    create_date: datetime
    slack_club_id: int

    class Config:
        orm_mode = True


# Tag schemas
class TagCreate(BaseModel):
    name: str
    slack_club_id: int


class TagUpdate(BaseModel):
    name: str


class TagDelete(BaseModel):
    id: int


# Note schemas
class NoteCreate(BaseModel):
    content: str
    slack_user_id: str
    slack_club_id: int
    private: Optional[bool]


class NoteUpdate(BaseModel):
    content: str
    private: Optional[bool]


class NoteAddTags(BaseModel):
    tags: List[int]


class NoteDelete(BaseModel):
    id: int


# Club schemas
class ClubCreate(BaseModel):
    book_title: str
    channel_id: str
    admin_user_id: str


class ClubUpdate(BaseModel):
    book_title: Optional[str] = None
    channel_id: Optional[str] = None
    is_active: Optional[bool] = None
    intro_message_ts: Optional[str] = None


class ClubDelete(BaseModel):
    id: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    locale: Optional[str] = None
    tz: Optional[str] = None


class UserDelete(BaseModel):
    slack_id_team_id: str


# Team schemas
class TeamCreate(TeamBase):
    team_id: str
    name: Optional[str] = None
    domain: Optional[str] = None
    email_domain: Optional[str] = None


class TeamDelete(BaseModel):
    team_id: str


# Main references to models via schemas
class Team(TeamBase):
    slack_users: List[UserBase]


class User(UserBase):
    slack_clubs: List[ClubBase]
    notes: List[NoteBase]


class Club(ClubBase):
    slack_users: List[UserBase]
    tags: List[TagBase]


class Clubs(BaseModel):
    clubs: List[Club]


class Note(NoteBase):
    tags: List[TagBase]
    slack_user: UserBase
    slack_club: ClubBase


class Notes(BaseModel):
    notes: List[Note]


class Tag(TagBase):
    slack_club: ClubBase
    notes: List[NoteBase]


class Tags(BaseModel):
    tags: List[Tag]
