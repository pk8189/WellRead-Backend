from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# load the database on startup
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # pylint: disable=no-member


@app.post("/user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(user, db)


@app.get("/user/{id}/", response_model=schemas.User)
def read_user(id: str, db: Session = Depends(get_db)):
    db_user = crud.read_user(id, db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user


@app.put("/user/{id}/", response_model=schemas.User)
def update_user(id: str, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(id, user, db)


@app.delete("/user/{id}/", response_model=schemas.UserDelete)
def delete_user(id: str, db: Session = Depends(get_db)):
    deleted_user = crud.delete_user(id, db)
    if deleted_user is None:
        raise HTTPException(status_code=400, detail="User not deleted, user not found")
    return deleted_user


@app.post("/club/", response_model=schemas.Club)
def create_club(club: schemas.ClubCreate, db: Session = Depends(get_db)):
    db_user = crud.read_user(club.admin_user_id, db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User creating club not found")
    return crud.create_club(club, db)


@app.get("/club/{club_id}/", response_model=schemas.Club)
def read_club(club_id: str, db: Session = Depends(get_db)):
    db_club = crud.read_club(club_id, db)
    if db_club is None:
        raise HTTPException(status_code=400, detail="Club not found")
    return db_club


@app.get("/club/", response_model=schemas.Clubs)
def read_clubs(user_id: Optional[str] = None, db: Session = Depends(get_db)):
    if user_id:
        return crud.read_clubs(db, user_id=user_id)
    return crud.read_clubs(db)


@app.put("/club/{club_id}/", response_model=schemas.Club)
def update_club(club_id: str, club: schemas.ClubUpdate, db: Session = Depends(get_db)):
    db_club = crud.update_club(club_id, club, db)
    return db_club


@app.put("/club/{club_id}/add_user/{user_id}/", response_model=schemas.Club)
def add_user_to_club(club_id: int, user_id: int, db: Session = Depends(get_db)):
    db_user = crud.read_user(user_id, db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    db_club = crud.read_club(club_id, db)
    if db_club is None:
        raise HTTPException(status_code=400, detail="Club not found")
    new_db_club = crud.add_user_to_club(club_id, user_id, db)
    return new_db_club


@app.delete("/club/{club_id}/", response_model=schemas.ClubDelete)
def delete_club(club_id: str, db: Session = Depends(get_db)):
    deleted_club = crud.delete_club(club_id, db)
    if delete_club is None:
        raise HTTPException(status_code=400, detail="Club not deleted, club not found")
    return deleted_club


@app.post("/note/", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    check_params = note.dict()
    db_user = crud.read_user(check_params["user_id"], db)
    db_club = crud.read_club(check_params["club_id"], db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User ID does not exist")
    if db_club is None:
        raise HTTPException(status_code=400, detail="Club ID does not exist")

    return crud.create_note(note, db)


@app.get("/note/{note_id}/", response_model=schemas.Note)
def read_note(note_id: str, db: Session = Depends(get_db)):
    db_note = crud.read_note(note_id, db)
    if db_note is None:
        raise HTTPException(status_code=400, detail="Note not found")
    return db_note


@app.get("/note/", response_model=schemas.Notes)
def read_notes(user_id: str, club_id: str, db: Session = Depends(get_db)):
    return crud.read_notes(user_id, club_id, db)


@app.put("/note/{note_id}/", response_model=schemas.Note)
def update_note(note_id: str, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    db_note = crud.read_note(note_id, db)
    if db_note is None:
        raise HTTPException(status_code=400, detail="Note not found")
    return crud.update_note(note_id, note, db)


@app.put("/note/{note_id}/tag/", response_model=schemas.Note)
def add_tags_to_notes(
    note_id: str, tags: schemas.NoteAddTags, db: Session = Depends(get_db)
):
    db_note = crud.read_note(note_id, db)
    for tag in tags.tags:
        db_tag = crud.read_tag(tag, db)
        if db_tag is None:
            raise HTTPException(status_code=400, detail="Tag not found")
    if db_note is None:
        raise HTTPException(status_code=400, detail="Note not found")
    return crud.add_tags_to_note(note_id, tags.tags, db)


@app.delete("/note/{note_id}/", response_model=schemas.NoteDelete)
def delete_note(note_id: str, db: Session = Depends(get_db)):
    deleted_note = crud.read_note(note_id, db)
    if deleted_note is None:
        raise HTTPException(status_code=400, detail="Note not deleted, note not found")
    return crud.delete_note(note_id, db)


@app.post("/tag/", response_model=schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    check_params = tag.dict()
    db_club = crud.read_club(check_params["club_id"], db)
    if db_club is None:
        raise HTTPException(status_code=400, detail="Club ID does not exist")
    duplicate_tag = crud.read_duplicate_tag(
        check_params["club_id"], check_params["name"], db,
    )
    if duplicate_tag:
        raise HTTPException(status_code=400, detail="Tag already exists")
    return crud.create_tag(tag, db)


@app.get("/tag/", response_model=schemas.Tags)
def read_tags(club_id: str, db: Session = Depends(get_db)):
    return crud.read_tags(club_id, db)


@app.get("/tag/{tag_id}/", response_model=schemas.Tag)
def read_tag(tag_id: str, db: Session = Depends(get_db)):
    db_tag = crud.read_tag(tag_id, db)
    if db_tag is None:
        raise HTTPException(status_code=400, detail="Tag not found")
    return db_tag


@app.put("/tag/{tag_id}/", response_model=schemas.Tag)
def update_tag(tag_id: str, tag: schemas.TagUpdate, db: Session = Depends(get_db)):
    db_tag = crud.read_tag(tag_id, db)
    if db_tag is None:
        raise HTTPException(status_code=400, detail="Tag not found")
    return crud.update_tag(tag_id, tag, db)


@app.delete("/tag/{tag_id}/", response_model=schemas.TagDelete)
def delete_tag(tag_id: str, db: Session = Depends(get_db)):
    deleted_tag = crud.read_tag(tag_id, db)
    if deleted_tag is None:
        raise HTTPException(status_code=400, detail="Tag not deleted, tag not found")
    return crud.delete_tag(tag_id, db)
