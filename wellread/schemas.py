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
    email: str
    name: str
    is_app_user: bool
    is_owner: bool
    locale: str
    profile_image_original: str
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
    next_meeting: Optional[datetime] = None

    class Config:
        orm_mode = True


class NoteBase(BaseModel):
    id: int
    create_date: datetime
    content: str
    slack_user_id: str
    slack_club_id: int

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


class NoteUpdate(BaseModel):
    content: str


class NoteAddTags(BaseModel):
    tags: List[int]


class NoteDelete(BaseModel):
    id: int


# Club schemas
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


class UserCreate(UserBase):
    slack_id_team_id: str
    email: str
    name: str
    is_app_user: bool
    is_owner: bool
    locale: str
    profile_image_original: str
    team_id: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    is_app_user: Optional[bool] = None
    is_owner: Optional[bool] = None
    locale: Optional[str] = None
    profile_image_original: Optional[str] = None


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


class Note(NoteBase):
    tags: List[TagBase]
    slack_user: UserBase
    slack_club: ClubBase


class Tag(TagBase):
    slack_club: ClubBase
    notes: List[NoteBase]


Tag.update_forward_refs()  # necessary to avoid recursion error in m2m orm_mode
