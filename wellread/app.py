from fastapi import FastAPI

from pydantic_models import NewClub, SlackWorkspace, User

app = FastAPI()


@app.post("/workspace/slack/")
async def create_slack_workspace(slack_workspace: SlackWorkspace):
    return slack_workspace


@app.post("/club/create/")
async def create_club(new_club: NewClub):
    return new_club


@app.post("/user/create/")
async def create_user(user: User):
    return user
