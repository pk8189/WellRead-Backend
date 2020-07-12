from sqlalchemy.orm import Session

from wellread import models, schemas


def create_team(team: schemas.TeamCreate, db: Session):
    db_team = models.SlackTeam(
        team_id=team.team_id,
        name=team.name,
        domain=team.domain,
        email_domain=team.email_domain,
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def get_team_by_id(team_id: str, db: Session):
    return (
        db.query(models.SlackTeam).filter(models.SlackTeam.team_id == team_id).first()
    )
