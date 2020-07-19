from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class UserBase(BaseModel):
    slack_id_team_id: str
    email: str
    name: str
    is_app_user: bool
    is_owner: bool
    locale: str
    profile_image_original: str
    team_id: str
    slack_clubs: Optional[list] = []


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


class User(UserBase):
    class Config:
        orm_mode = True
