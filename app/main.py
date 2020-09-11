from datetime import timedelta
from random import choices
from string import ascii_uppercase, digits
from time import time
from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import (
    auth_utils,
    crud,
    dependencies,
    google_books,
    google_books_schemas,
    models,
    schemas,
)
from app.database import engine
from app.logging import logger

# create DB
models.Base.metadata.create_all(bind=engine)


# init the application
app = FastAPI(debug=engine.name == "sqlite")


# Log all HTTP requests
@app.middleware("http")
async def log_requests(request, call_next):
    idem = "".join(choices(ascii_uppercase + digits, k=6))
    logger.info(f"request_id={idem} start request path={request.url.path}")
    start_time = time()

    response = await call_next(request)
    breakpoint()
    process_time = (time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
    )

    return response


@app.post("/api/token", response_model=schemas.Token)
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


@app.post("/api/user/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, db: Session = Depends(dependencies.get_db),
):
    return crud.create_user(user, db)


@app.get("/api/user/", response_model=schemas.User)
def read_user(user: schemas.User = Depends(dependencies.get_current_user),):
    return user


@app.put("/api/user/book/{book_id}/add/", response_model=schemas.User)
def add_book_to_user(
    book_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.update_user_add_book(user.id, book_id, db)


@app.put("/api/user/book/{book_id}/remove/", response_model=schemas.User)
def remove_book_from_user(
    book_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.update_user_remove_boook(user.id, book_id, db)


@app.put("/api/user/relationship/{user_id}/follow/", response_model=schemas.UserFollow)
def follow_user(
    user_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.follow_user(user.id, user_id, db)


@app.put(
    "/api/user/relationship/{user_id}/unfollow/", response_model=schemas.UserFollow
)
def unfollow_user(
    user_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.unfollow_user(user.id, user_id, db)


@app.post("/api/book/", response_model=schemas.Book)
def get_or_create_book(
    book: schemas.BookCreate,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    """If the book already exists in the backend, add this user"""
    return crud.get_or_create_book(user.id, book, db)


@app.get("/api/book/google_books/{q}", response_model=google_books_schemas.Volumes)
def query_google_books(
    q: str, user: schemas.User = Depends(dependencies.get_current_user),
):
    assert user.id
    return google_books_schemas.Volumes(volumes=google_books.query_google_books(q))


@app.get(
    "/api/book/{book_id}/google_book/", response_model=google_books_schemas.VolumeRes
)
def get_google_book_data(
    book_id: str,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    assert user.id
    db_book = crud.read_book(user.id, book_id, db)
    return google_books.get_google_book(db_book.google_books_id)


@app.get("/api/book/{book_id}/", response_model=schemas.Book)
def read_book(
    book_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_book(user.id, book_id, db)


@app.post("/api/club/", response_model=schemas.Club)
def create_club(
    club: schemas.ClubCreate,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.create_club(user.id, club, db)


@app.get("/api/club/{club_id}/", response_model=schemas.Club)
def read_club(
    club_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_club(user.id, club_id, db)


@app.get("/api/clubs/", response_model=schemas.Clubs)
def read_clubs(
    is_active: bool = True,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_clubs(user.id, is_active, db)


@app.put("/api/club/{club_id}/", response_model=schemas.Club)
def update_club(
    club: schemas.ClubUpdate,
    club_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.update_club(user.id, club_id, club, db)


@app.put("/api/club/{club_id}/join/", response_model=schemas.Club)
def club_user_join(
    club_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.add_user_to_club(club_id, user.id, db)


@app.put("/api/club/{club_id}/leave/", response_model=schemas.Club)
def club_user_leave(
    club_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.remove_user_from_club(club_id, user.id, db)


@app.put("/api/club/{club_id}/book/{book_id}/add/", response_model=schemas.Club)
def club_book_add(
    club_id: int,
    book_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.add_book_to_club(user.id, club_id, book_id, db)


@app.put("/api/club/{club_id}/book/{book_id}/remove/", response_model=schemas.Club)
def club_book_remove(
    club_id: int,
    book_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.remove_book_from_club(user.id, club_id, book_id, db)


@app.delete("/api/club/{club_id}/", response_model=schemas.ClubDelete)
def delete_club(
    club_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.delete_club(user.id, club_id, db)


@app.post("/api/note/", response_model=schemas.Note)
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.create_note(user.id, note, db)


@app.get("/api/note/{note_id}/", response_model=schemas.Note)
def read_note(
    note_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_note(user.id, note_id, db)


@app.get("/api/notes/me/", response_model=schemas.Notes)
def read_my_notes(
    book_id: int,
    include_private: bool = True,
    include_archived: bool = False,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_my_notes(user.id, book_id, include_private, include_archived, db)


@app.put("/api/note/{note_id}/", response_model=schemas.Note)
def update_note(
    note_id: int,
    note: schemas.NoteUpdate,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.update_note(user.id, note_id, note, db)


@app.put("/api/note/{note_id}/tag/", response_model=schemas.Note)
def add_tags_to_notes(
    note_id: int,
    tags: schemas.NoteAddTagsAndClubTags,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.add_tags_to_note(user.id, note_id, tags, db)


@app.delete("/api/note/{note_id}/", response_model=schemas.NoteDelete)
def delete_note(
    note_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.delete_note(user.id, note_id, db)


@app.post("/api/tag/", response_model=schemas.Tag)
def create_tag(
    tag: schemas.TagCreate,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.create_tag(user.id, tag, db)


@app.get("/api/tag/{tag_id}/", response_model=schemas.Tag)
def read_tag(
    tag_id: int,
    book_id: Optional[int] = None,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_tag(user.id, tag_id, book_id, db)


@app.get("/api/tags/", response_model=schemas.Tags)
def read_tags(
    archived: bool = False,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_tags(user.id, archived, db)


@app.put("/api/tag/{tag_id}/", response_model=schemas.Tag)
def update_tag(
    tag: schemas.TagUpdate,
    tag_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.update_tag(user.id, tag_id, tag, db)


@app.delete("/api/tag/{tag_id}/", response_model=schemas.TagDelete)
def delete_tag(
    tag_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.delete_tag(user.id, tag_id, db)


@app.post("/api/club_tag/", response_model=schemas.ClubTag)
def create_club_tag(
    club_tag: schemas.ClubTagCreate,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.create_club_tag(user.id, club_tag, db)


@app.get("/api/club_tag/{club_tag_id}/", response_model=schemas.ClubTag)
def read_club_tag(
    club_tag_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_club_tag(user.id, club_tag_id, db)


@app.get("/api/club_tags/", response_model=schemas.ClubTags)
def read_club_tags(
    club_id: int,
    book_id: Optional[int] = None,
    archived: bool = False,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.read_club_tags(user.id, club_id, book_id, archived, db)


@app.put("/api/club_tag/{club_tag_id}/", response_model=schemas.ClubTag)
def update_club_tag(
    club_tag_id: int,
    club_tag: schemas.ClubTagUpdate,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.update_club_tag(user.id, club_tag_id, club_tag, db)


@app.delete("/api/club_tag/{club_tag_id}/", response_model=schemas.ClubTagDelete)
def delete_club_tag(
    club_tag_id: int,
    db: Session = Depends(dependencies.get_db),
    user: schemas.User = Depends(dependencies.get_current_user),
):
    return crud.delete_club_tag(user.id, club_tag_id, db)
