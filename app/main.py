from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import auth_utils, crud, models, schemas  # pylint: disable=no-name-in-module
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

# load the database on startup
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # pylint: disable=no-member


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(auth_utils.oauth2_scheme),
):
    email = auth_utils.decode_jwt(token)
    user = crud.get_user_auth(email, db)
    if user is None:
        raise auth_utils.credentials_exception
    return user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db),
):
    user = auth_utils.authenticate_user(db, form_data.username, form_data.password,)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/user/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db),
):
    db_user = crud.get_user_by_email(user.email, db)
    if db_user is not None:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )
    return crud.create_user(user, db)


@app.get("/user/", response_model=schemas.User)
def read_user(
    user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db),
):
    db_user = crud.read_user(user.id, db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user


@app.put("/user/", response_model=schemas.User)
def update_user(
    updated_user: schemas.UserUpdate,
    user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.update_user(user.id, updated_user, db)


@app.post("/club/", response_model=schemas.Club)
def create_club(
    club: schemas.ClubCreate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.create_club(user.id, club, db)


@app.get("/club/{club_id}/", response_model=schemas.Club)
def read_club(
    club_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    db_club = crud.read_club(user.id, club_id, db)
    if db_club is None:
        raise HTTPException(status_code=400, detail="Club not found")
    return db_club


@app.get("/club/", response_model=schemas.Clubs)
def read_clubs(
    db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user),
):
    return crud.read_clubs(user.id, db)


@app.put("/club/{club_id}/", response_model=schemas.Club)
def update_club(
    club_id: int,
    club: schemas.ClubUpdate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.update_club(club_id, club, db)


@app.put("/club/{club_id}/join/", response_model=schemas.Club)
def user_join(
    club_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    db_user = crud.read_user(user.id, db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    db_club = crud.read_clubs_for_joining(club_id, db)
    if db_club is None:
        raise HTTPException(status_code=400, detail="Club not found")
    new_db_club = crud.add_user_to_club(club_id, user.id, db)
    return new_db_club


@app.delete("/club/{club_id}/", response_model=schemas.ClubDelete)
def delete_club(
    club_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    db_club = crud.read_club(user.id, club_id, db)
    if db_club.admin_user_id != user.id:
        raise HTTPException(
            status_code=400, detail="Club not deleted, user is not admin",
        )
    deleted_club = crud.delete_club(club_id, db)
    if delete_club is None:
        raise HTTPException(
            status_code=400, detail="Club not deleted, club not found",
        )
    return deleted_club


@app.post("/note/", response_model=schemas.Note)
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    check_params = note.dict()
    db_club = crud.read_club(user.id, check_params["club_id"], db)
    if db_club is None:
        raise HTTPException(status_code=400, detail="Club ID does not exist")
    return crud.create_note(user.id, note, db)


@app.get("/note/{note_id}/", response_model=schemas.Note)
def read_note(
    note_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    """
    Get note data (if note is private, you must be the note owner)
    """
    db_note = crud.read_note(user.id, note_id, db)
    return db_note


@app.get("/note/", response_model=schemas.Notes)
def read_notes(
    club_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    """
    Return all notes for a club which are neither private nor archived
    """
    return crud.read_notes(club_id, db)


@app.put("/note/{note_id}/", response_model=schemas.Note)
def update_note(
    note_id: int,
    note: schemas.NoteUpdate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    db_note = crud.update_note(user.id, note_id, note, db)
    if not db_note:
        raise HTTPException(status_code=400, detail="Note not found")
    return db_note


@app.put("/note/{note_id}/tag/", response_model=schemas.Note)
def add_tags_to_notes(
    note_id: int,
    tags: schemas.NoteAddTags,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    db_note = crud.read_note(user.id, note_id, db)
    for tag in tags.tags:
        db_tag = crud.read_tag(tag, db)
        if db_tag is None:
            raise HTTPException(status_code=400, detail="Tag not found")
    if db_note is None:
        raise HTTPException(status_code=400, detail="Note not found")
    return crud.add_tags_to_note(user.id, note_id, tags.tags, db)


@app.delete("/note/{note_id}/", response_model=schemas.NoteDelete)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    deleted_note = crud.delete_note(user.id, note_id, db)
    if deleted_note is None:
        raise HTTPException(status_code=400, detail="Note not deleted")
    return deleted_note


@app.post("/tag/", response_model=schemas.Tag)
def create_tag(
    tag: schemas.TagCreate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    check_params = tag.dict()
    db_club = crud.read_club(user.id, check_params["club_id"], db)
    if db_club is None:
        raise HTTPException(status_code=400, detail="Club ID does not exist")
    duplicate_tag = crud.read_duplicate_tag(
        check_params["club_id"], check_params["name"], db,
    )
    if duplicate_tag:
        raise HTTPException(status_code=400, detail="Tag with this name already exists")
    return crud.create_tag(tag, db)


@app.get("/tag/", response_model=schemas.Tags)
def read_tags(
    club_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    db_club = crud.read_club(user.id, club_id, db)
    if not db_club:
        raise HTTPException(status_code=400, detail="User not authorized to read tag")
    return crud.read_tags(club_id, db)


@app.get("/tag/{tag_id}/", response_model=schemas.Tag)
def read_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    db_tag = crud.read_tag(tag_id, db)
    if db_tag is None:
        raise HTTPException(status_code=400, detail="Tag not found")
    return db_tag


@app.put("/tag/{tag_id}/", response_model=schemas.Tag)
def update_tag(
    tag_id: int,
    tag: schemas.TagUpdate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    db_tag = crud.read_tag(tag_id, db)
    if db_tag is None:
        raise HTTPException(status_code=400, detail="Tag not found")
    return crud.update_tag(tag_id, tag, db)


@app.delete("/tag/{tag_id}/", response_model=schemas.TagDelete)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    tag_to_delete = crud.read_tag(tag_id, db)
    if tag_to_delete is None:
        raise HTTPException(status_code=400, detail="Tag not deleted, tag not found")
    return crud.delete_tag(tag_id, db)
