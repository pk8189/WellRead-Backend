from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class TeamBase(BaseModel):
    team_id: str
    name: Optional[str] = None
    domain: Optional[str] = None
    email_domain: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class TeamDelete(BaseModel):
    team_id: str


class UserBase(BaseModel):
    slack_id_team_id: str
    email: str
    name: str
    is_app_user: bool
    is_owner: bool
    locale: str
    profile_image_original: str
    team_id: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    is_app_user: Optional[bool] = None
    is_owner: Optional[bool] = None
    locale: Optional[str] = None
    profile_image_original: Optional[str] = None


class UserDelete(BaseModel):
    slack_id_team_id: str


class ClubBase(BaseModel):
    book_title: str
    admin_user_id: str
    channel_id: str


class ClubCreate(ClubBase):
    pass


class User(UserBase):
    class Config:
        orm_mode = True


class Club(ClubBase):
    id: int
    create_date: datetime
    is_active: bool
    admin_user_id: str
    slack_users: List[User] = []
    next_meeting: Optional[datetime] = None

    class Config:
        orm_mode = True


class Team(TeamBase):
    slack_users: List[User] = []

    class Config:
        orm_mode = True
