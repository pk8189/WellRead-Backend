from sqlalchemy.orm import Session

from wellread import models, schemas


# SlackTeam CREATE
def create_team(team: schemas.TeamCreate, db: Session):
    db_team = models.SlackTeam(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


# SlackTeam READ
def read_team(team_id: str, db: Session):
    return (
        db.query(models.SlackTeam).filter(models.SlackTeam.team_id == team_id).first()
    )


# SlackTeam UPDATE (not needed yet)

# SlackTeam DELETE
def delete_team(team_id: str, db: Session):
    db.query(models.SlackTeam).filter(models.SlackTeam.team_id == team_id).delete()
    db.commit()
    return {"team_id": team_id}


# SlackUser CREATE
def create_user(user: schemas.UserCreate, db: Session):
    db_user = models.SlackUser(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# SlackUser READ
def read_user(slack_id_team_id: str, db: Session):
    return (
        db.query(models.SlackUser)
        .filter(models.SlackUser.slack_id_team_id == slack_id_team_id)
        .first()
    )


# SlackUser UPDATE
def update_user(slack_id_team_id: str, user: schemas.UserUpdate, db: Session):
    db_user = (
        db.query(models.SlackUser)
        .filter(models.SlackUser.slack_id_team_id == slack_id_team_id)
        .first()
    )
    remove_nones = {k: v for k, v in user.dict().items() if v is not None}
    db_user.update(remove_nones)
    db.commit()
    db.refresh(db_user)
    return db_user


# SlackUser DELETE
def delete_user(slack_id_team_id: str, db: Session):
    db.query(models.SlackUser).filter(
        models.SlackUser.slack_id_team_id == slack_id_team_id
    ).delete()
    db.commit()
    return {"slack_id_team_id": slack_id_team_id}


# SlackClub CREATE
def create_club(club: schemas.ClubCreate, db: Session):
    db_club = models.SlackClub(**club.dict())
    db.add(db_club)
    db.commit()
    db.refresh(db_club)
    return db_club


# SlackClub READ
def read_club(club_id: str, db: Session):
    return db.query(models.SlackClub).filter(models.SlackClub.id == club_id).first()


# SlackClub READ
def read_clubs(db: Session, slack_id_team_id: str = None):
    if not slack_id_team_id:
        return {"clubs": db.query(models.SlackClub).all()}
    query_results = (
        db.query(models.SlackClub)
        .filter(
            models.SlackClub.slack_users.any(
                models.SlackUser.slack_id_team_id == slack_id_team_id
            )
        )
        .all()
    )
    return {"clubs": query_results}


# SlackClub UPDATE
def update_club(club_id: str, club: schemas.ClubUpdate, db: Session):
    db_club = db.query(models.SlackClub).filter(models.SlackClub.id == club_id).first()
    remove_nones = {k: v for k, v in club.dict().items() if v is not None}
    db_club.update(remove_nones)
    db.commit()
    db.refresh(db_club)
    return db_club


# SlackClub UPDATE
def add_user_to_club(club_id: str, slack_id_team_id: str, db: Session):
    db_club = db.query(models.SlackClub).filter(models.SlackClub.id == club_id).first()
    db_user = (
        db.query(models.SlackUser)
        .filter(models.SlackUser.slack_id_team_id == slack_id_team_id)
        .first()
    )
    db_club.slack_users.append(db_user)
    db.commit()
    db.refresh(db_club)
    return db_club


# SlackClub DELETE
def delete_club(club_id: str, db: Session):
    db.query(models.SlackClub).filter(models.SlackClub.id == club_id).delete()
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
def read_tags(club_id: str, db: Session):
    query_results = (
        db.query(models.Tag).filter(models.Tag.slack_club_id == club_id).all()
    )
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
