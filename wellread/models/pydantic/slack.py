from datetime import datetime
from typing import List

from pydantic import BaseModel

from wellread.models.pydantic import common


class SlackWorkspace(BaseModel):
    slack_app_id: str
    bot_id: str

    class Config:
        orm_mode = True


class SlackClub(BaseModel):
    slack_workspace: SlackWorkspace
    channel_id: str
    book_title: str
    intro_message_ts: int
    admin_id: str
    next_meeting_date: datetime = None

    class Config:
        orm_mode = True


class SlackUser(BaseModel):
    user: common.User
    slack_id: str
    profile_img_url: str
    clubs: List[SlackClub] = None

    class Config:
        orm_mode = True
