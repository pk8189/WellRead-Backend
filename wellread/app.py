from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from wellread import crud, models, schemas
from wellread.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# load the database on startup
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # pylint: disable=no-member


@app.post("/team/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = crud.read_team(team.team_id, db)
    if db_team:
        raise HTTPException(status_code=400, detail="Team already exists")
    return crud.create_team(team, db)


@app.get("/team/{team_id}/", response_model=schemas.Team)
def read_team(team_id: str, db: Session = Depends(get_db)):
    db_team = crud.read_team(team_id, db)
    if db_team is None:
        raise HTTPException(status_code=400, detail="Team not found")
    return db_team


@app.delete("/team/{team_id}/", response_model=schemas.TeamDelete)
def delete_team(team_id: str, db: Session = Depends(get_db)):
    deleted_team = crud.delete_team(team_id, db)
    if deleted_team is None:
        raise HTTPException(
            status_code=400, detail="Team not deleted, it was not found"
        )
    return deleted_team


@app.post("/user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.read_user(user.slack_id_team_id, db)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    db_team = crud.read_team(user.team_id, db)
    if not db_team:
        raise HTTPException(
            status_code=400,
            detail=f"No team exists for specified team_id: {user.team_id}",
        )
    return crud.create_user(user, db)


@app.get("/user/{slack_id_team_id}/", response_model=schemas.User)
def read_user(slack_id_team_id: str, db: Session = Depends(get_db)):
    db_user = crud.read_user(slack_id_team_id, db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user


@app.put("/user/{slack_id_team_id}/", response_model=schemas.User)
def update_user(
    slack_id_team_id: str, user: schemas.UserUpdate, db: Session = Depends(get_db)
):
    return crud.update_user(slack_id_team_id, user, db)


@app.delete("/user/{slack_id_team_id}/", response_model=schemas.UserDelete)
def delete_user(slack_id_team_id: str, db: Session = Depends(get_db)):
    deleted_user = crud.delete_user(slack_id_team_id, db)
    if deleted_user is None:
        raise HTTPException(status_code=400, detail="User not deleted, user not found")
    return deleted_user


@app.post("/club/", response_model=schemas.Club)
def create_club(club: schemas.ClubCreate, db: Session = Depends(get_db)):
    db_user = crud.read_user(club.admin_user_id, db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User creating club not found")
    return crud.create_club(club, db)


@app.get("/club/{club_id}/", response_model=schemas.Club)
def read_club(club_id: str, db: Session = Depends(get_db)):
    db_club = crud.read_club(club_id, db)
    if db_club is None:
        raise HTTPException(status_code=400, detail="Club not found")
    return db_club


@app.put("/club/{club_id}/", response_model=schemas.Club)
def update_club(club_id: str, club: schemas.ClubUpdate, db: Session = Depends(get_db)):
    db_club = crud.update_club(club_id, club, db)
    return db_club


@app.put("/club/{club_id}/add_user/{slack_id_team_id}/", response_model=schemas.Club)
def add_user_to_club(
    club_id: str, slack_id_team_id: str, db: Session = Depends(get_db)
):
    db_user = crud.read_user(slack_id_team_id, db)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    db_club = crud.read_club(club_id, db)
    if db_club is None:
        raise HTTPException(status_code=400, detail="Club not found")
    new_db_club = crud.add_user_to_club(club_id, slack_id_team_id, db)
    return new_db_club


@app.delete("/club/{club_id}/", response_model=schemas.ClubDelete)
def delete_club(club_id: str, db: Session = Depends(get_db)):
    deleted_club = crud.delete_club(club_id, db)
    if delete_club is None:
        raise HTTPException(status_code=400, detail="Club not deleted, club not found")
    return deleted_club
