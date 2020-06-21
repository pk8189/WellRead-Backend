from fastapi import FastAPI

from wellread.models.pydantic.common import Note, Tag
from wellread.models.pydantic.slack import SlackClub, SlackUser, SlackWorkspace

app = FastAPI()


@app.post("/workspace/slack/create/")
async def create_slack_workspace(slack_workspace: SlackWorkspace):
    return slack_workspace


@app.post("/club/create/")
async def create_club(club: SlackClub):
    return club


@app.post("/user/create/")
async def create_user(user: SlackUser):
    return user


@app.post("/tag/create/")
async def create_tag(tag: Tag):
    return Tag


@app.post("/note/create")
async def create_note(note: Note):
    return Note
