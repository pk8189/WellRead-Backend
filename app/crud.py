from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import auth_utils, models, schemas


# User AUTH
def get_user_auth(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


# User CREATE
def create_user(user: schemas.UserCreate, db: Session):
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
def read_user(id: str, db: Session):
    return db.query(models.User).filter(models.User.id == id).first()


# User READ
def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


# User UPDATE
def update_user(id: str, user: schemas.UserUpdate, db: Session):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    remove_nones = {k: v for k, v in user.dict().items() if v is not None}
    db_user.update(remove_nones)
    db.commit()
    db.refresh(db_user)
    return db_user


# Club CREATE
def create_club(user_id: int, club: schemas.ClubCreate, db: Session):
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
def read_club(user_id: int, club_id: int, db: Session):
    return (
        db.query(models.Club)
        .filter(models.Club.id == club_id)
        .filter(models.Club.users.any(models.User.id == user_id))
        .first()
    )


# Club READ
def read_clubs(
    user_id: int, db: Session,
):
    query_results = (
        db.query(models.Club)
        .filter(models.Club.users.any(models.User.id == user_id))
        .all()
    )
    return {"clubs": query_results}


# Club READ
def read_clubs_for_joining(club_id: int, db: Session):
    # TODO permissions for invited users
    return db.query(models.Club).filter(models.Club.id == club_id).first()


# Club UPDATE
def update_club(club_id: str, club: schemas.ClubUpdate, db: Session):
    db_club = db.query(models.Club).filter(models.Club.id == club_id).first()
    remove_nones = {k: v for k, v in club.dict().items() if v is not None}
    db_club.update(remove_nones)
    db.commit()
    db.refresh(db_club)
    return db_club


# Club UPDATE
def add_user_to_club(club_id: str, id: str, db: Session):
    db_club = db.query(models.Club).filter(models.Club.id == club_id).first()
    db_user = db.query(models.User).filter(models.User.id == id).first()
    db_club.users.append(db_user)
    db.commit()
    db.refresh(db_club)
    return db_club


# Club DELETE
def delete_club(club_id: str, db: Session):
    db_club = db.query(models.Club).filter(models.Club.id == club_id).first()
    db.delete(db_club)
    db.commit()
    return db_club


# Note CREATE
def create_note(user_id: int, note: schemas.NoteCreate, db: Session):
    note_dict = note.dict()
    note_dict["user_id"] = user_id
    db_note = models.Note(**note_dict)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


# Note READ
def read_note(user_id: int, note_id: int, db: Session):
    """
    Get a note by ID if the user is in the club the note was written in
    and if the note is private, ensure that the user requesting the note
    wrote the note.
    """
    db_note = (
        db.query(models.Note, models.Club)
        .filter(models.Note.id == note_id)
        .filter(models.Club.users.any(models.User.id == user_id))
        .first()
    )
    if not db_note:
        raise HTTPException(status_code=400, detail="Note not found")
    if db_note.Note.private == True and db_note.Note.user_id != user_id:
        raise HTTPException(status_code=401, detail="Not authorized")
    return db_note.Note


# Note READ
def read_team_notes(club_id: int, archived: bool, db: Session):
    query_results = (
        db.query(models.Note)
        .filter(models.Note.club_id == club_id)
        .filter(models.Note.private == False)  # only return public notes
    )
    if not archived:
        query_results = query_results.filter(models.Note.archived == False)
    return {"notes": query_results.all()}


# Note READ
def read_personal_notes(
    user_id: int, club_id: int, private: bool, archived: bool, db: Session,
):
    query_results = (
        db.query(models.Note)
        .filter(models.Note.user_id == user_id)
        .filter(models.Note.club_id == club_id)
    )
    if not private:
        query_results = query_results.filter(models.Note.private == False)
    if not archived:
        query_results = query_results.filter(models.Note.archived == False)
    return {"notes": query_results.all()}


# Note UPDATE
def update_note(user_id: int, note_id: int, note: schemas.NoteUpdate, db: Session):
    db_note = (
        db.query(models.Note)
        .filter(models.Note.id == note_id)
        .filter(models.Note.user_id == user_id)
        .first()
    )
    remove_nones = {k: v for k, v in note.dict().items() if v is not None}
    db_note.update(remove_nones)
    db.commit()
    db.refresh(db_note)
    return db_note


# Note UPDATE
def add_tags_to_note(user_id: int, note_id: int, tag_ids: list, db: Session):
    db_note = (
        db.query(models.Note)
        .filter(models.Note.id == note_id)
        .filter(models.Note.user_id == user_id)
        .first()
    )
    for tag_id in tag_ids:
        db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
        db_note.tags.append(db_tag)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


# Note DELETE
def delete_note(user_id: int, note_id: int, db: Session):
    db_note = (
        db.query(models.Note)
        .filter(models.Note.user_id == user_id)
        .filter(models.Note.id == note_id)
        .first()
    )
    db.delete(db_note)
    db.commit()
    return db_note


# Tag CREATE
def create_tag(tag: schemas.TagCreate, db: Session):
    db_tag = models.Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


# Tag READ
def read_tag(tag_id: str, db: Session):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()


# Tag READ
def read_duplicate_tag(club_id: int, name: str, db: Session):
    return (
        db.query(models.Tag)
        .filter(models.Tag.club_id == club_id)
        .filter(models.Tag.name == name)
        .first()
    )


# Tag READ
def read_tags(club_id: str, db: Session):
    query_results = db.query(models.Tag).filter(models.Tag.club_id == club_id).all()
    return {"tags": query_results}


# Tag UPDATE
def update_tag(tag_id: str, tag: schemas.TagUpdate, db: Session):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    remove_nones = {k: v for k, v in tag.dict().items() if v is not None}
    db_tag.update(remove_nones)
    db.commit()
    db.refresh(db_tag)
    return db_tag


# Tag DELETE
def delete_tag(tag_id: str, db: Session):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    db.delete(db_tag)
    db.commit()
    return db_tag
