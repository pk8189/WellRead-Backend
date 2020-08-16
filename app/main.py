from datetime import timedelta

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import auth_utils, crud, models, schemas
from app.database import SessionLocal, engine
from app.permissions import Club, Note, Tag, User

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def user_can_create(
    user: schemas.UserCreate, db: Session = Depends(get_db),
) -> schemas.UserCreate:
    User(db).email_not_in_use(user.email)
    return user


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(auth_utils.oauth2_scheme),
) -> schemas.DBUser:
    email = auth_utils.decode_jwt(token)
    user = crud.get_user_auth(email, db)
    if user is None:
        raise auth_utils.credentials_exception
    return user


async def tag_is_admin(
    tag_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
) -> int:
    Tag(db, user, tag_id).is_admin()
    return tag_id


async def club_is_admin(
    club_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
) -> int:
    Club(db, user, club_id).is_admin()
    return club_id


async def club_is_member(
    club_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
) -> int:
    Club(db, user, club_id).read()
    return club_id


async def club_is_invited(
    club_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
) -> int:
    Club(db, user, club_id).is_invited()
    return club_id


async def note_is_valid(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
) -> schemas.NoteCreate:
    Club(db, user, note.club_id).exists()
    return note


async def note_can_read(
    note_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
) -> int:
    Note(db, user, note_id).can_read()
    return note_id


async def note_can_update(
    note_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
) -> int:
    Note(db, user, note_id).can_update()
    return note_id


async def tags_read(
    tags: schemas.NoteAddTags,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
) -> schemas.NoteAddTags:
    [Tag(db, user, tag_id).read() for tag_id in tags.tags]
    return tags


async def note_can_delete(
    note_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
) -> int:
    Note(db, user, note_id).can_delete()
    return note_id


async def tag_can_create(
    tag: schemas.TagCreate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
) -> schemas.TagCreate:
    Club(db, user, tag.club_id).duplicate_tag(tag.name)
    return tag


async def tag_can_read(
    tag_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
) -> int:
    Tag(db, user, tag_id).can_read()
    return tag_id


async def tag_is_admin(
    tag_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
) -> int:
    Tag(db, user, tag_id).is_admin()
    return tag_id


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db),
):
    user = auth_utils.authenticate_user(db, form_data.username, form_data.password,)
    access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/user/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db),
):
    return crud.create_user(user, db)


@app.get("/user/", response_model=schemas.User)
def read_user(
    user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db),
):
    return user


@app.post("/club/", response_model=schemas.Club)
def create_club(
    club: schemas.ClubCreate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.create_club(user.id, club, db)


@app.get("/club/{club_id}/", response_model=schemas.Club)
def read_club(
    club_id: int = Depends(club_is_member),
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.read_club(user.id, club_id, db)


@app.get("/clubs/", response_model=schemas.Clubs)
def read_clubs(
    is_active: bool = True,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.read_clubs(user.id, is_active, db)


@app.put("/club/{club_id}/", response_model=schemas.Club)
def update_club(
    club: schemas.ClubUpdate,
    club_id: int = Depends(club_is_admin),
    db: Session = Depends(get_db),
):
    return crud.update_club(club_id, club, db)


@app.put("/club/{club_id}/join/", response_model=schemas.Club)
def user_join(
    club_id: int = Depends(club_is_invited),
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.add_user_to_club(club_id, user.id, db)


@app.delete("/club/{club_id}/", response_model=schemas.ClubDelete)
def delete_club(
    club_id: int = Depends(club_is_admin), db: Session = Depends(get_db),
):
    return crud.delete_club(club_id, db)


@app.post("/note/", response_model=schemas.Note)
def create_note(
    note: schemas.NoteCreate = Depends(note_is_valid),
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.create_note(user.id, note, db)


@app.get("/note/{note_id}/", response_model=schemas.Note)
def read_note(
    note_id: int = Depends(note_can_read),
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.read_note(user.id, note_id, db)


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
    return crud.read_team_notes(user.id, club_id, archived, db)


@app.put("/note/{note_id}/", response_model=schemas.Note)
def update_note(
    note: schemas.NoteUpdate,
    note_id: int = Depends(note_can_update),
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.update_note(user.id, note_id, note, db)


@app.put("/note/{note_id}/tag/", response_model=schemas.Note)
def add_tags_to_notes(
    tags: schemas.NoteAddTags = Depends(tags_read),
    note_id: int = Depends(note_can_update),
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.add_tags_to_note(user.id, note_id, tags.tags, db)


@app.delete("/note/{note_id}/", response_model=schemas.NoteDelete)
def delete_note(
    note_id: int = Depends(note_can_delete),
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.delete_note(user.id, note_id, db)


@app.post("/tag/", response_model=schemas.Tag)
def create_tag(
    tag: schemas.TagCreate = Depends(tag_can_create), db: Session = Depends(get_db),
):
    return crud.create_tag(tag, db)


@app.get("/tags/", response_model=schemas.Tags)
def read_tags(
    archived: bool = False,
    club_id: int = Depends(club_is_member),
    db: Session = Depends(get_db),
):
    return crud.read_tags(club_id, archived, db)


@app.get("/tag/{tag_id}/", response_model=schemas.Tag)
def read_tag(
    tag_id: int = Depends(tag_can_read),
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.read_tag(user.id, tag_id, db)


@app.put("/tag/{tag_id}/", response_model=schemas.Tag)
def update_tag(
    tag: schemas.TagUpdate,
    tag_id: int = Depends(tag_is_admin),
    db: Session = Depends(get_db),
):
    return crud.update_tag(tag_id, tag, db)


@app.delete("/tag/{tag_id}/", response_model=schemas.TagDelete)
def delete_tag(
    tag_id: int = Depends(tag_is_admin), db: Session = Depends(get_db),
):
    return crud.delete_tag(tag_id, db)
