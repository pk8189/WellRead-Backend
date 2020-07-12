from typing import List, Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class TeamBase(BaseModel):
    team_id: str
    name: Optional[str] = None
    domain: Optional[str] = None
    email_domain: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class TeamDelete(TeamBase):
    pass


class UserBase(BaseModel):
    slack_id_team_id: str
    email: str
    name: str
    is_app_user: bool
    is_owner: bool
    locale: str
    profile_image_original: str


class UserCreate(UserBase):
    team_id: str


class User(UserBase):
    class Config:
        orm_mode = True


class Team(TeamBase):

    users: List[User] = []

    class Config:
        orm_mode = True
