from sqlalchemy.orm import Session

from app import models, schemas


# User CREATE
def create_user(user: schemas.UserCreate, db: Session):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# User READ
def read_user(id: str, db: Session):
    return db.query(models.User).filter(models.User.id == id).first()


# User UPDATE
def update_user(id: str, user: schemas.UserUpdate, db: Session):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    remove_nones = {k: v for k, v in user.dict().items() if v is not None}
    db_user.update(remove_nones)
    db.commit()
    db.refresh(db_user)
    return db_user


# User DELETE
def delete_user(id: str, db: Session):
    db.query(models.User).filter(models.User.id == id).delete()
    db.commit()
    return {"id": id}


# Club CREATE
def create_club(club: schemas.ClubCreate, db: Session):
    db_club = models.Club(**club.dict())
    db.add(db_club)
    db.commit()
    db.refresh(db_club)
    return db_club


# Club READ
def read_club(club_id: str, db: Session):
    return db.query(models.Club).filter(models.Club.id == club_id).first()


# Club READ
def read_clubs(db: Session, user_id: int = None):
    if not user_id:
        return {"clubs": db.query(models.Club).all()}
    query_results = (
        db.query(models.Club)
        .filter(models.Club.users.any(models.User.id == user_id))
        .all()
    )
    return {"clubs": query_results}


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
    return {"id": club_id}


# Note CREATE
def create_note(note: schemas.NoteCreate, db: Session):
    db_note = models.Note(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


# Note READ
def read_note(note_id: str, db: Session):
    return db.query(models.Note).filter(models.Note.id == note_id).first()


# Note READ
def read_notes(id: str, club_id: str, db: Session):
    query_results = (
        db.query(models.Note)
        .filter(models.Note.user_id == id)
        .filter(models.Note.club_id == club_id)
        .all()
    )
    return {"notes": query_results}


# Note UPDATE
def update_note(note_id: str, note: schemas.NoteUpdate, db: Session):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    remove_nones = {k: v for k, v in note.dict().items() if v is not None}
    db_note.update(remove_nones)
    db.commit()
    db.refresh(db_note)
    return db_note


# Note UPDATE
def add_tags_to_note(note_id: str, tag_ids: list, db: Session):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    for tag_id in tag_ids:
        db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
        db_note.tags.append(db_tag)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


# Note DELETE
def delete_note(note_id: str, db: Session):
    db.query(models.Note).filter(models.Note.id == note_id).delete()
    db.commit()
    return {"id": note_id}


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
    db.query(models.Tag).filter(models.Tag.id == tag_id).delete()
    db.commit()
    return {"id": tag_id}
