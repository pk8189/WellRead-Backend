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
