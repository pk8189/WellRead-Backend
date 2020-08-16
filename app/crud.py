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
    return (
        db.query(models.Club)
        .filter(models.Club.id == club_id)
        .filter(models.Club.users.any(models.User.id == user_id))
        .first()
    )


# Club READ without user query
def read_clubs_for_joining(club_id: int, db: Session) -> schemas.Club:
    return db.query(models.Club).filter(models.Club.id == club_id).first()


# Club READ
def read_clubs(user_id: int, is_active: bool, db: Session,) -> schemas.Clubs:
    query_results = db.query(models.Club).filter(
        models.Club.users.any(models.User.id == user_id)
    )
    if is_active:
        query_results = query_results.filter(models.Club.is_active == True)
    return schemas.Clubs(clubs=query_results.all())


# Club UPDATE
def update_club(club_id: int, club: schemas.ClubUpdate, db: Session) -> schemas.Club:
    db_club = db.query(models.Club).filter(models.Club.id == club_id).first()
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


# Club DELETE
def delete_club(club_id: int, db: Session) -> schemas.Club:
    db_club = db.query(models.Club).filter(models.Club.id == club_id).first()
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
    db_note = (
        db.query(models.Note, models.Club)
        .filter(models.Note.id == note_id)
        .filter(models.Club.users.any(models.User.id == user_id))
        .first()
    )
    if db_note:
        return db_note.Note


# Note READ
def read_team_notes(
    user_id: int, club_id: int, archived: bool, db: Session
) -> schemas.Notes:
    query_results = (
        db.query(models.Note, models.Club)
        .filter(models.Note.club_id == club_id)
        .filter(models.Club.users.any(models.User.id == user_id))
        .filter(models.Note.private == False)  # only return public notes
    )
    if not archived:
        query_results = query_results.filter(models.Note.archived == False)
    results = [qr.Note for qr in query_results.all()]
    return schemas.Notes(notes=results)


# Note READ
def read_personal_notes(
    user_id: int, club_id: int, private: bool, archived: bool, db: Session,
) -> schemas.Notes:
    query_results = (
        db.query(models.Note)
        .filter(models.Note.user_id == user_id)
        .filter(models.Note.club_id == club_id)
    )
    if not private:
        query_results = query_results.filter(models.Note.private == False)
    if not archived:
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
    remove_nones = {k: v for k, v in note.dict().items() if v is not None}
    db_note.update(remove_nones)
    db.commit()
    db.refresh(db_note)
    return db_note


# Note UPDATE
def add_tags_to_note(
    user_id: int, note_id: int, tag_ids: list, db: Session
) -> schemas.Note:
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
def delete_note(user_id: int, note_id: int, db: Session) -> schemas.Note:
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
def create_tag(tag: schemas.TagCreate, db: Session) -> schemas.Tag:
    db_tag = models.Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


# Tag READ
def read_tag(user_id: int, tag_id: int, db: Session) -> schemas.Tag:
    db_tag = (
        db.query(models.Tag, models.User)
        .filter(models.Tag.id == tag_id)
        .filter(models.Club.users.any(models.User.id == user_id))
        .first()
    )
    if db_tag:
        return db_tag.Tag


# Tag READ
def read_duplicate_tag(club_id: int, name: str, db: Session) -> schemas.Tag:
    return (
        db.query(models.Tag)
        .filter(models.Tag.club_id == club_id)
        .filter(models.Tag.name == name)
        .first()
    )


# Tag READ
def read_tags(club_id: int, archived: bool, db: Session) -> schemas.Tags:
    query_results = db.query(models.Tag).filter(models.Tag.club_id == club_id)
    if not archived:
        query_results = query_results.filter(models.Tag.archived == False)
    return schemas.Tags(tags=query_results.all())


# Tag UPDATE
def update_tag(tag_id: int, tag: schemas.TagUpdate, db: Session) -> schemas.Tag:
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    remove_nones = {k: v for k, v in tag.dict().items() if v is not None}
    db_tag.update(remove_nones)
    db.commit()
    db.refresh(db_tag)
    return db_tag


# Tag DELETE
def delete_tag(tag_id: int, db: Session) -> schemas.Tag:
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    db.delete(db_tag)
    db.commit()
    return db_tag
