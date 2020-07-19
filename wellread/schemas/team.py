from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class TeamBase(BaseModel):
    team_id: str
    name: Optional[str] = None
    domain: Optional[str] = None
    email_domain: Optional[str] = None
    slack_users: Optional[list] = []


class TeamCreate(TeamBase):
    team_id: str
    name: Optional[str] = None
    domain: Optional[str] = None
    email_domain: Optional[str] = None


class TeamDelete(BaseModel):
    team_id: str


class Team(TeamBase):
    class Config:
        orm_mode = True
