from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import auth_utils, models, schemas


# User AUTH
def get_user_auth(email: str, db: Session) -> schemas.DBUser:
    return db.query(models.User).filter(models.User.email == email).first()


# User CREATE
def create_user(user: schemas.UserCreate, db: Session) -> schemas.User:
    user_dict = user.dict()
    password = user_dict["password"]
    user_dict["hashed_password"] = auth_utils.get_password_hash(password)
    del user_dict["password"]
    db_user = models.User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# User READ
def read_user(id: int, db: Session) -> schemas.User:
    return db.query(models.User).filter(models.User.id == id).first()


# User READ
def get_user_by_email(email: str, db: Session) -> schemas.User:
    return db.query(models.User).filter(models.User.email == email).first()


# User UPDATE
def update_user_add_book(user_id: int, book_id: int, db: Session) -> schemas.User:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db_user.books.append(db_book)
    db.commit()
    db.refresh(db_user)
    return db_user


# User UPDATE
def update_user_remove_boook(user_id: int, book_id: int, db: Session) -> schemas.User:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db_user.books.remove(db_book)
    db.commit()
    db.refresh(db_user)
    return db_user


# User UPDATE
def follow_user(follower_id: int, following_id: int, db: Session) -> schemas.User:
    follower_user = db.query(models.User).filter(models.User.id == follower_id).first()
    following_user = (
        db.query(models.User).filter(models.User.id == following_id).first()
    )
    following_user.followers.append(follower_user)
    db.commit()
    db.refresh(following_user)
    return schemas.UserFollow(id=following_user.id, full_name=following_user.full_name)


# User UPDATE
def unfollow_user(follower_id: int, following_id: int, db: Session) -> schemas.User:
    follower_user = db.query(models.User).filter(models.User.id == follower_id).first()
    unfollowed_user = (
        db.query(models.User).filter(models.User.id == following_id).first()
    )
    unfollowed_user.followers.remove(follower_user)
    db.commit()
    db.refresh(unfollowed_user)
    return schemas.UserFollow(
        id=unfollowed_user.id, full_name=unfollowed_user.full_name
    )


# Book CREATE
def get_or_create_book(
    used_id: int, book: schemas.BookCreate, db: Session
) -> schemas.Book:
    db_book = (
        db.query(models.Book)
        .filter(models.Book.google_books_id == book.google_books_id)
        .first()
    )
    if not db_book:
        db_book = models.Book(**book.dict())
    db_user = db.query(models.User).filter(models.User.id == used_id).first()
    db.add(db_book)
    db_book.users.append(db_user)
    db.commit()
    db.refresh(db_book)
    return db_book


# Book READ
def read_book(user_id: int, book_id: int, db: Session) -> schemas.Book:
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    return db_book


# Club CREATE
def create_club(user_id: int, club: schemas.ClubCreate, db: Session) -> schemas.Club:
    club_dict = club.dict()
    club_dict["admin_user_id"] = user_id
    db_club = models.Club(**club_dict)
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_club.users.append(db_user)
    db.add(db_club)
    db.commit()
    db.refresh(db_club)
    return db_club


# Club READ
def read_club(user_id: int, club_id: int, db: Session) -> schemas.Club:
    db_query = (
        db.query(models.Club)
        .filter(models.Club.id == club_id)
        .filter(models.Club.users.any(models.User.id == user_id))
        .first()
    )
    if not db_query:
        raise HTTPException(status_code=400, detail="Club not found")
    return db_query


# Club READ
def read_clubs(user_id: int, is_active: bool, db: Session,) -> schemas.Clubs:
    query_results = db.query(models.Club).filter(
        models.Club.users.any(models.User.id == user_id)
    )
    if is_active:
        query_results = query_results.filter(models.Club.is_active == True)
    return schemas.Clubs(clubs=query_results.all())


# Club UPDATE
def update_club(
    user_id: int, club_id: int, club: schemas.ClubUpdate, db: Session
) -> schemas.Club:
    db_club = (
        db.query(models.Club)
        .filter(models.Club.id == club_id)
        .filter(models.Club.users.any(models.User.id == user_id))
        .first()
    )
    if not db_club:
        raise HTTPException(status_code=400, detail="Club not found")
    remove_nones = {k: v for k, v in club.dict().items() if v is not None}
    db_club.update(remove_nones)
    db.commit()
    db.refresh(db_club)
    return db_club


# Club UPDATE
def add_user_to_club(club_id: int, user_id: int, db: Session) -> schemas.Club:
    db_club = db.query(models.Club).filter(models.Club.id == club_id).first()
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_club.users.append(db_user)
    db.commit()
    db.refresh(db_club)
    return db_club


# Club UPDATE
def remove_user_from_club(club_id: int, user_id: int, db: Session) -> schemas.Club:
    db_club = db.query(models.Club).filter(models.Club.id == club_id).first()
    if db_club.admin_user_id == user_id:
        raise HTTPException(status_code=400, detail="Admin cannot leave club")
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_club.users.remove(db_user)
    db.commit()
    db.refresh(db_club)
    return db_club


# Club UPDATE
def add_book_to_club(
    user_id: int, club_id: int, book_id: int, db: Session
) -> schemas.Club:
    db_club = (
        db.query(models.Club)
        .filter(models.Club.id == club_id)
        .filter(models.Club.users.any(models.User.id == user_id))
        .first()
    )
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db_club.books.append(db_book)
    db.commit()
    db.refresh(db_club)
    return db_club


# Club UPDATE
def remove_book_from_club(
    user_id: int, club_id: int, book_id: int, db: Session
) -> schemas.Club:
    db_club = db.query(models.Club).filter(models.Club.id == club_id).first()
    if db_club.admin_user_id != user_id:
        raise HTTPException(
            status_code=400, detail="Non-admin cannot remove book from club"
        )
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db_club.books.remove(db_book)
    db.commit()
    db.refresh(db_club)
    return db_club


# Club DELETE
def delete_club(user_id: int, club_id: int, db: Session) -> schemas.Club:
    db_club = db.query(models.Club).filter(models.Club.id == club_id).first()
    if db_club.admin_user_id != user_id:
        raise HTTPException(status_code=403, detail="Non-admin cannot delete club")
    db.delete(db_club)
    db.commit()
    return db_club


# Note CREATE
def create_note(user_id: int, note: schemas.NoteCreate, db: Session) -> schemas.Note:
    note_dict = note.dict()
    note_dict["user_id"] = user_id
    db_note = models.Note(**note_dict)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


# Note READ
def read_note(user_id: int, note_id: int, db: Session) -> schemas.Note:
    """
    Get a note by ID if the user is in the club the note was written in
    and if the note is private, ensure that the user requesting the note
    wrote the note.
    """
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(400, detail="Note not found")
    if db_note.user_id != user_id and db_note.private:
        raise HTTPException(403, detail="Cannot read private note")
    return db_note


# Note READ
def read_my_notes(
    user_id: int,
    book_id: int,
    include_private: bool,
    include_archived: bool,
    db: Session,
) -> schemas.Notes:
    query_results = db.query(models.Note).filter(models.Note.user_id == user_id)
    if book_id:
        query_results = query_results.filter(models.Note.book_id == book_id)
    if not include_private:
        query_results = query_results.filter(models.Note.private == False)
    if not include_archived:
        query_results = query_results.filter(models.Note.archived == False)
    return schemas.Notes(notes=query_results.all())


# Note UPDATE
def update_note(
    user_id: int, note_id: int, note: schemas.NoteUpdate, db: Session
) -> schemas.Note:
    db_note = (
        db.query(models.Note)
        .filter(models.Note.id == note_id)
        .filter(models.Note.user_id == user_id)
        .first()
    )
    if not db_note:
        raise HTTPException(status_code=400, detail="Note not found")
    remove_nones = {k: v for k, v in note.dict().items() if v is not None}
    db_note.update(remove_nones)
    db.commit()
    db.refresh(db_note)
    return db_note


# Note UPDATE
def add_tags_to_note(
    user_id: int, note_id: int, tags: schemas.NoteAddTagsAndClubTags, db: Session
) -> schemas.Note:
    db_note = (
        db.query(models.Note)
        .filter(models.Note.id == note_id)
        .filter(models.Note.user_id == user_id)
        .first()
    )
    if not db_note:
        raise HTTPException(status_code=400, detail="Note not found")
    for tag_id in tags.tags:
        db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
        if not db_tag:
            raise HTTPException(status_code=400, detail="Tag not found")
        db_note.tags.append(db_tag)
    for club_tag_id in tags.club_tags:
        db_club_tag = (
            db.query(models.ClubTag).filter(models.ClubTag.id == club_tag_id).first()
        )
        if not db_club_tag:
            raise HTTPException(status_code=400, detail="ClubTag not found")
        db_note.club_tags.append(db_club_tag)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


# Note UPDATE
def remove_tags_from_note(
    user_id: int, note_id: int, tags: schemas.NoteAddTagsAndClubTags, db: Session
) -> schemas.Note:
    db_note = (
        db.query(models.Note)
        .filter(models.Note.id == note_id)
        .filter(models.Note.user_id == user_id)
        .first()
    )
    if not db_note:
        raise HTTPException(status_code=400, detail="Note not found")
    for tag_id in tags.tags:
        db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
        if not db_tag:
            raise HTTPException(status_code=400, detail="Tag not found")
        db_note.tags.remove(db_tag)
    for club_tag_id in tags.club_tags:
        db_club_tag = (
            db.query(models.ClubTag).filter(models.ClubTag.id == club_tag_id).first()
        )
        if not db_club_tag:
            raise HTTPException(status_code=400, detail="ClubTag not found")
        db_note.club_tags.remove(db_club_tag)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


# Note DELETE
def delete_note(user_id: int, note_id: int, db: Session) -> schemas.Note:
    db_note = (
        db.query(models.Note)
        .filter(models.Note.user_id == user_id)
        .filter(models.Note.id == note_id)
        .first()
    )
    if not db_note:
        raise HTTPException(status_code=400, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return db_note


# Tag CREATE
def create_tag(user_id: int, tag: schemas.TagCreate, db: Session) -> schemas.Tag:
    tag_dict = tag.dict()
    tag_dict["user_id"] = user_id
    db_tag = models.Tag(**tag_dict)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


# Tag READ
def read_tag(user_id: int, tag_id: int, book_id: int, db: Session) -> schemas.Tag:
    db_query = (
        db.query(models.Tag)
        .filter(models.Tag.id == tag_id)
        .filter(models.Tag.user_id == user_id)
    )
    if book_id:
        db_query.filter(models.Tag.books.any(models.Book.id == book_id))
    if not db_query.first():
        raise HTTPException(status_code=400, detail="Tag not found")
    return db_query.first()


# Tag READ
def read_tags(user_id: int, archived: bool, db: Session) -> schemas.Tags:
    query_results = db.query(models.Tag).filter(models.Tag.user_id == user_id)
    if not archived:
        query_results = query_results.filter(models.Tag.archived == False)
    return schemas.Tags(tags=query_results.all())


# Tag UPDATE
def update_tag(
    user_id: int, tag_id: int, tag: schemas.TagUpdate, db: Session
) -> schemas.Tag:
    db_tag = (
        db.query(models.Tag)
        .filter(models.Tag.id == tag_id)
        .filter(models.Tag.user_id == user_id)
        .first()
    )
    if not db_tag:
        raise HTTPException(status_code=400, detail="Tag not found")
    remove_nones = {k: v for k, v in tag.dict().items() if v is not None}
    db_tag.update(remove_nones)
    db.commit()
    db.refresh(db_tag)
    return db_tag


# Tag DELETE
def delete_tag(user_id: int, tag_id: int, db: Session) -> schemas.Tag:
    db_tag = (
        db.query(models.Tag)
        .filter(models.Tag.id == tag_id)
        .filter(models.Tag.user_id == user_id)
        .first()
    )
    if not db_tag:
        raise HTTPException(status_code=400, detail="Tag not found")
    db.delete(db_tag)
    db.commit()
    return db_tag


# ClubTag CREATE
def create_club_tag(
    user_id: int, club_tag: schemas.TagCreate, db: Session
) -> schemas.ClubTag:
    db_club = (
        db.query(models.Club)
        .filter(models.Club.id == club_tag.club_id)
        .filter(models.Club.users.any(models.User.id == user_id))
        .first()
    )
    if not db_club:
        raise HTTPException(status_code=400, detail="Club not found")
    db_club_tag = models.ClubTag(**club_tag.dict())
    db.add(db_club_tag)
    db.commit()
    db.refresh(db_club_tag)
    return db_club_tag


# ClubTag READ
def read_club_tag(user_id: int, club_tag_id: int, db: Session) -> schemas.ClubTag:
    db_query = db.query(models.ClubTag).filter(models.ClubTag.id == club_tag_id).first()
    if not db_query:
        raise HTTPException(status_code=400, detail="ClubTag not found")
    return db_query


# ClubTag READ
def read_club_tags(
    user_id: int, club_id: int, book_id: int, archived: bool, db: Session
) -> schemas.ClubTags:
    query_results = (
        db.query(models.ClubTag)
        .filter(models.ClubTag.club_id == club_id)
        .filter(models.Club.users.any(models.User.id == user_id))
    )
    if book_id:
        query_results = query_results.filter(models.ClubTag.book_id == book_id)
    if not archived:
        query_results = query_results.filter(models.ClubTag.archived == False)

    if not query_results.all():
        raise HTTPException(status_code=400, detail="ClubTag not found")
    return schemas.ClubTags(club_tags=query_results.all())


# ClubTag UPDATE
def update_club_tag(
    user_id: int, club_tag_id: int, club_tag: schemas.ClubTagUpdate, db: Session
) -> schemas.ClubTag:
    db_club_tag = (
        db.query(models.ClubTag)
        .filter(models.ClubTag.id == club_tag_id)
        .filter(models.Club.admin_user_id == user_id)
        .first()
    )
    if not db_club_tag:
        raise HTTPException(status_code=400, detail="ClubTag not found")
    remove_nones = {k: v for k, v in club_tag.dict().items() if v is not None}
    db_club_tag.update(remove_nones)
    db.commit()
    db.refresh(db_club_tag)
    return db_club_tag


# ClubTag DELETE
def delete_club_tag(user_id: int, club_tag_id: int, db: Session) -> schemas.ClubTag:
    db_club_tag = (
        db.query(models.ClubTag)
        .filter(models.ClubTag.id == club_tag_id)
        .filter(models.Club.admin_user_id == user_id)
        .first()
    )
    if not db_club_tag:
        raise HTTPException(status_code=400, detail="ClubTag not found")
    db.delete(db_club_tag)
    db.commit()
    return db_club_tag
