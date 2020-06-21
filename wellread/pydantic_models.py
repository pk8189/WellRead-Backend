from datetime import datetime

from pydantic import BaseModel


class SlackWorkspace(BaseModel):
    slack_app_id: str
    bot_id: str


class NewClub(BaseModel):
    channel_id: str
    book_title: str
    intro_message_ts: int
    next_meeting_date: datetime
    admin_id: str


class User(BaseModel):
    slack_id: str
    club_id: str
    profile_img_url: str
