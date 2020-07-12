from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class TeamBase(BaseModel):
    team_id: str
    name: Optional[str] = None
    domain: Optional[str] = None
    email_domain: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    team_id: str
    name: str
    domain: str
    email_domain: str

    class Config:
        orm_mode = True
