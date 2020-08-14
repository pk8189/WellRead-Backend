from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import auth_utils, crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(auth_utils.oauth2_scheme),
) -> schemas.User:
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
    """
    Unauthenticated endpoint to create users.
    Block the user if the email already exists
    """
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
    """Get the current users data"""
    db_user = crud.read_user(user.id, db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user


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


@app.get("/clubs/", response_model=schemas.Clubs)
def read_clubs(
    is_active: bool = True,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.read_clubs(user.id, is_active, db)


@app.put("/club/{club_id}/", response_model=schemas.Club)
def update_club(
    club_id: int,
    club: schemas.ClubUpdate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    db_club = crud.read_club(user.id, club_id, db)
    if db_club is None:
        raise HTTPException(status_code=400, detail="Club not found")
    if db_club.admin_user_id != user.id:
        raise HTTPException(
            status_code=400, detail="Club not updated, user is not admin",
        )
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


@app.get("/notes/me/", response_model=schemas.Notes)
def read_my_notes(
    club_id: int,
    private: bool = False,
    archived: bool = False,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.read_personal_notes(user.id, club_id, private, archived, db)


@app.get("/notes/club/", response_model=schemas.Notes)
def read_team_notes(
    club_id: int,
    archived: bool = False,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.read_team_notes(club_id, archived, db)


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
        db_tag = crud.read_tag(user.id, tag, db)
        if db_tag is None:
            raise HTTPException(status_code=400, detail="Tag not found")
    if db_note is None:
        raise HTTPException(status_code=400, detail="Note not found")
    if db_note.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to tag note")
    return crud.add_tags_to_note(user.id, note_id, tags.tags, db)


@app.delete("/note/{note_id}/", response_model=schemas.NoteDelete)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    db_note = crud.read_note(user.id, note_id, db)
    if db_note is None:
        raise HTTPException(status_code=400, detail="Note not found")
    if db_note.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete note")
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
    if not db_club:
        raise HTTPException(status_code=400, detail="Club does not exist or not member")
    duplicate_tag = crud.read_duplicate_tag(
        check_params["club_id"], check_params["name"], db,
    )
    if duplicate_tag:
        raise HTTPException(status_code=400, detail="Tag with this name already exists")
    return crud.create_tag(tag, db)


@app.get("/tags/", response_model=schemas.Tags)
def read_tags(
    club_id: int,
    archived: bool = False,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    """Read all tags for a club if user is in club (optional archived flag)"""
    db_club = crud.read_club(user.id, club_id, db)
    if not db_club:
        raise HTTPException(status_code=403, detail="User not authorized to read tags")
    return crud.read_tags(club_id, archived, db)


@app.get("/tag/{tag_id}/", response_model=schemas.Tag)
def read_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    """Read tag by ID if user is corresponding club"""
    db_tag = crud.read_tag(user.id, tag_id, db)
    if not db_tag:
        raise HTTPException(status_code=400, detail="Tag not found")
    return db_tag


@app.put("/tag/{tag_id}/", response_model=schemas.Tag)
def update_tag(
    tag_id: int,
    tag: schemas.TagUpdate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    """Club admins can update Tag data"""
    db_tag = crud.read_tag(user.id, tag_id, db)
    if db_tag is None:
        raise HTTPException(status_code=400, detail="Tag not found")
    club_id = db_tag.club_id
    db_club = crud.read_club(user.id, club_id, db)
    if user.id != db_club.admin_user_id:
        raise HTTPException(status_code=403, detail="User not authorized to update tag")
    return crud.update_tag(tag_id, tag, db)


@app.delete("/tag/{tag_id}/", response_model=schemas.TagDelete)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    tag_to_delete = crud.read_tag(user.id, tag_id, db)
    if tag_to_delete is None:
        raise HTTPException(status_code=400, detail="Tag not deleted, tag not found")
    club_id = tag_to_delete.club_id
    db_club = crud.read_club(user.id, club_id, db)
    if user.id != db_club.admin_user_id:
        raise HTTPException(status_code=403, detail="User not authorized to delete tag")
    return crud.delete_tag(tag_id, db)
