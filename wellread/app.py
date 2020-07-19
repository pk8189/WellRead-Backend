from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from wellread import crud, models
from wellread.database import SessionLocal, engine
from wellread.schemas import club as club_schemas
from wellread.schemas import note as note_schemas
from wellread.schemas import tag as tag_schemas
from wellread.schemas import team as team_schemas
from wellread.schemas import user as user_schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# load the database on startup
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # pylint: disable=no-member


@app.post("/team/", response_model=team_schemas.Team)
def create_team(team: team_schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = crud.read_team(team.team_id, db)
    if db_team:
        raise HTTPException(status_code=400, detail="Team already exists")
    return crud.create_team(team, db)


@app.get("/team/{team_id}/", response_model=team_schemas.Team)
def read_team(team_id: str, db: Session = Depends(get_db)):
    db_team = crud.read_team(team_id, db)
    if db_team is None:
        raise HTTPException(status_code=400, detail="Team not found")
    return db_team


@app.delete("/team/{team_id}/", response_model=team_schemas.TeamDelete)
def delete_team(team_id: str, db: Session = Depends(get_db)):
    deleted_team = crud.delete_team(team_id, db)
    if deleted_team is None:
        raise HTTPException(
            status_code=400, detail="Team not deleted, it was not found"
        )
    return deleted_team


@app.post("/user/", response_model=user_schemas.User)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.read_user(user.slack_id_team_id, db)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    db_team = crud.read_team(user.team_id, db)
    if not db_team:
        raise HTTPException(
            status_code=400,
            detail=f"No team exists for specified team_id: {user.team_id}",
        )
    return crud.create_user(user, db)


@app.get("/user/{slack_id_team_id}/", response_model=user_schemas.User)
def read_user(slack_id_team_id: str, db: Session = Depends(get_db)):
    db_user = crud.read_user(slack_id_team_id, db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user


@app.put("/user/{slack_id_team_id}/", response_model=user_schemas.User)
def update_user(
    slack_id_team_id: str, user: user_schemas.UserUpdate, db: Session = Depends(get_db)
):
    return crud.update_user(slack_id_team_id, user, db)


@app.delete("/user/{slack_id_team_id}/", response_model=user_schemas.UserDelete)
def delete_user(slack_id_team_id: str, db: Session = Depends(get_db)):
    deleted_user = crud.delete_user(slack_id_team_id, db)
    if deleted_user is None:
        raise HTTPException(status_code=400, detail="User not deleted, user not found")
    return deleted_user


@app.post("/club/", response_model=club_schemas.Club)
def create_club(club: club_schemas.ClubCreate, db: Session = Depends(get_db)):
    db_user = crud.read_user(club.admin_user_id, db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User creating club not found")
    return crud.create_club(club, db)


@app.get("/club/{club_id}/", response_model=club_schemas.Club)
def read_club(club_id: str, db: Session = Depends(get_db)):
    db_club = crud.read_club(club_id, db)
    if db_club is None:
        raise HTTPException(status_code=400, detail="Club not found")
    return db_club


@app.put("/club/{club_id}/", response_model=club_schemas.Club)
def update_club(
    club_id: str, club: club_schemas.ClubUpdate, db: Session = Depends(get_db)
):
    db_club = crud.update_club(club_id, club, db)
    return db_club


@app.put(
    "/club/{club_id}/add_user/{slack_id_team_id}/", response_model=club_schemas.Club
)
def add_user_to_club(
    club_id: str, slack_id_team_id: str, db: Session = Depends(get_db)
):
    db_user = crud.read_user(slack_id_team_id, db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    db_club = crud.read_club(club_id, db)
    if db_club is None:
        raise HTTPException(status_code=400, detail="Club not found")
    new_db_club = crud.add_user_to_club(club_id, slack_id_team_id, db)
    return new_db_club


@app.delete("/club/{club_id}/", response_model=club_schemas.ClubDelete)
def delete_club(club_id: str, db: Session = Depends(get_db)):
    deleted_club = crud.delete_club(club_id, db)
    if delete_club is None:
        raise HTTPException(status_code=400, detail="Club not deleted, club not found")
    return deleted_club


@app.post("/note/", response_model=note_schemas.Note)
def create_note(note: note_schemas.NoteCreate, db: Session = Depends(get_db)):
    check_params = note.dict()
    db_user = crud.read_user(check_params["slack_user_id"], db)
    db_club = crud.read_club(check_params["slack_club_id"], db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User ID does not exist")
    if db_club is None:
        raise HTTPException(status_code=400, detail="Club ID does not exist")

    return crud.create_note(note, db)


@app.get("/note/{note_id}/", response_model=note_schemas.Note)
def read_note(note_id: str, db: Session = Depends(get_db)):
    db_note = crud.read_note(note_id, db)
    if db_note is None:
        raise HTTPException(status_code=400, detail="Note not found")
    return db_note


@app.put("/note/{note_id}/", response_model=note_schemas.Note)
def update_note(
    note_id: str, note: note_schemas.NoteUpdate, db: Session = Depends(get_db)
):
    db_note = crud.read_note(note_id, db)
    if db_note is None:
        raise HTTPException(status_code=400, detail="Note not found")
    return crud.update_note(note_id, note, db)


@app.put("/note/{note_id}/tag/", response_model=note_schemas.Note)
def add_tags_to_notes(
    note_id: str, tags: note_schemas.NoteAddTags, db: Session = Depends(get_db)
):
    db_note = crud.read_note(note_id, db)
    for tag in tags.tags:
        db_tag = crud.read_tag(tag, db)
        if db_tag is None:
            raise HTTPException(status_code=400, detail="Tag not found")
    if db_note is None:
        raise HTTPException(status_code=400, detail="Note not found")
    return crud.add_tags_to_note(note_id, tags.tags, db)


@app.delete("/note/{note_id}/", response_model=note_schemas.NoteDelete)
def delete_note(note_id: str, db: Session = Depends(get_db)):
    deleted_note = crud.read_note(note_id, db)
    if deleted_note is None:
        raise HTTPException(status_code=400, detail="Note not deleted, note not found")
    return crud.delete_note(note_id, db)


@app.post("/tag/", response_model=tag_schemas.Tag)
def create_tag(tag: tag_schemas.TagCreate, db: Session = Depends(get_db)):
    check_params = tag.dict()
    db_club = crud.read_club(check_params["slack_club_id"], db)
    if db_club is None:
        raise HTTPException(status_code=400, detail="Club ID does not exist")
    return crud.create_tag(tag, db)


@app.get("/tag/{tag_id}/", response_model=tag_schemas.Tag)
def read_tag(tag_id: str, db: Session = Depends(get_db)):
    db_tag = crud.read_tag(tag_id, db)
    if db_tag is None:
        raise HTTPException(status_code=400, detail="Tag not found")
    return db_tag


@app.put("/tag/{tag_id}/", response_model=tag_schemas.Tag)
def update_tag(tag_id: str, tag: tag_schemas.TagUpdate, db: Session = Depends(get_db)):
    db_tag = crud.read_tag(tag_id, db)
    if db_tag is None:
        raise HTTPException(status_code=400, detail="Tag not found")
    return crud.update_tag(tag_id, tag, db)


@app.delete("/tag/{tag_id}/", response_model=tag_schemas.TagDelete)
def delete_tag(tag_id: str, db: Session = Depends(get_db)):
    deleted_tag = crud.read_tag(tag_id, db)
    if deleted_tag is None:
        raise HTTPException(status_code=400, detail="Tag not deleted, tag not found")
    return crud.delete_tag(tag_id, db)
