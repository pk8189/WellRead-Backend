from fastapi import Depends
from sqlalchemy.orm import Session

from app import auth_utils, crud, schemas
from app.database import SessionLocal
from app.permissions import Club, Note, Tag, User


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
