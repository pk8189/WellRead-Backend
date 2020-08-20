from datetime import timedelta
from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import auth_utils, crud, dependencies, models, schemas
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(dependencies.get_db),
):
    user = auth_utils.authenticate_user(db, form_data.username, form_data.password,)
    access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/user/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, db: Session = Depends(dependencies.get_db),
):
    return crud.create_user(user, db)


@app.get("/user/", response_model=schemas.User)
def read_user(user: schemas.User = Depends(dependencies.get_current_user),):
    return user


@app.put("/user/book/{book_id}/add/", response_model=schemas.User)
def add_book_to_user(
    book_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.update_user_add_book(user.id, book_id, db)


@app.put("/user/book/{book_id}/remove/", response_model=schemas.User)
def remove_book_from_user(
    book_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.update_user_remove_boook(user.id, book_id, db)


@app.post("/book/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.create_book(user.id, book, db)


@app.get("/book/{book_id}/", response_model=schemas.Book)
def read_book(
    book_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_book(user.id, book_id, db)


@app.post("/club/", response_model=schemas.Club)
def create_club(
    club: schemas.ClubCreate,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.create_club(user.id, club, db)


@app.get("/club/{club_id}/", response_model=schemas.Club)
def read_club(
    club_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_club(user.id, club_id, db)


@app.get("/clubs/", response_model=schemas.Clubs)
def read_clubs(
    is_active: bool = True,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_clubs(user.id, is_active, db)


@app.put("/club/{club_id}/", response_model=schemas.Club)
def update_club(
    club: schemas.ClubUpdate,
    club_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.update_club(user.id, club_id, club, db)


@app.put("/club/{club_id}/join/", response_model=schemas.Club)
def club_user_join(
    club_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.add_user_to_club(club_id, user.id, db)


@app.put("/club/{club_id}/leave/", response_model=schemas.Club)
def club_user_leave(
    club_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.remove_user_from_club(club_id, user.id, db)


@app.put("/club/{club_id}/book/{book_id}/add/", response_model=schemas.Club)
def club_book_add(
    club_id: int,
    book_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.add_book_to_club(user.id, club_id, book_id, db)


@app.put("/club/{club_id}/book/{book_id}/remove/", response_model=schemas.Club)
def club_book_remove(
    club_id: int,
    book_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.remove_book_from_club(user.id, club_id, book_id, db)


@app.delete("/club/{club_id}/", response_model=schemas.ClubDelete)
def delete_club(
    club_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.delete_club(user.id, club_id, db)


@app.post("/note/", response_model=schemas.Note)
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.create_note(user.id, note, db)


@app.get("/note/{note_id}/", response_model=schemas.Note)
def read_note(
    note_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_note(user.id, note_id, db)


@app.get("/notes/me/", response_model=schemas.Notes)
def read_my_notes(
    book_id: int,
    include_private: bool = True,
    include_archived: bool = False,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_my_notes(user.id, book_id, include_private, include_archived, db)


@app.put("/note/{note_id}/", response_model=schemas.Note)
def update_note(
    note_id: int,
    note: schemas.NoteUpdate,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.update_note(user.id, note_id, note, db)


@app.put("/note/{note_id}/tag/", response_model=schemas.Note)
def add_tags_to_notes(
    note_id: int,
    tags: schemas.NoteAddTagsAndClubTags,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.add_tags_to_note(user.id, note_id, tags, db)


@app.delete("/note/{note_id}/", response_model=schemas.NoteDelete)
def delete_note(
    note_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.delete_note(user.id, note_id, db)


@app.post("/tag/", response_model=schemas.Tag)
def create_tag(
    tag: schemas.TagCreate,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.create_tag(user.id, tag, db)


@app.get("/tag/{tag_id}/", response_model=schemas.Tag)
def read_tag(
    tag_id: int,
    book_id: Optional[int] = None,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_tag(user.id, tag_id, book_id, db)


@app.get("/tags/", response_model=schemas.Tags)
def read_tags(
    archived: bool = False,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_tags(user.id, archived, db)


@app.put("/tag/{tag_id}/", response_model=schemas.Tag)
def update_tag(
    tag: schemas.TagUpdate,
    tag_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.update_tag(user.id, tag_id, tag, db)


@app.delete("/tag/{tag_id}/", response_model=schemas.TagDelete)
def delete_tag(
    tag_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.delete_tag(user.id, tag_id, db)


@app.post("/club_tag/", response_model=schemas.ClubTag)
def create_club_tag(
    club_tag: schemas.ClubTagCreate,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.create_club_tag(user.id, club_tag, db)


@app.get("/club_tag/{club_tag_id}/", response_model=schemas.ClubTag)
def read_club_tag(
    club_tag_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_club_tag(user.id, club_tag_id, db)


@app.get("/club_tags/", response_model=schemas.ClubTags)
def read_club_tags(
    club_id: int,
    book_id: Optional[int],
    archived: bool = False,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_club_tags(user.id, club_id, book_id, archived, db)


@app.put("/club_tag/{club_tag_id}/", response_model=schemas.ClubTag)
def update_club_tag(
    club_tag_id: int,
    club_tag: schemas.ClubTagUpdate,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.update_club_tag(user.id, club_tag_id, club_tag, db)


@app.delete("/club_tag/{club_tag_id}/", response_model=schemas.ClubTagDelete)
def delete_club_tag(
    tag_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.delete_club_tag(user.id, tag_id, db)
