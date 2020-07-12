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
    db_team = crud.get_team_by_id(team.team_id, db)
    if db_team:
        raise HTTPException(status_code=400, detail="Team already exists")
    return crud.create_team(team, db)


@app.get("/team/{team_id}", response_model=schemas.Team)
def read_team(team_id: str, db: Session = Depends(get_db)):
    db_team = crud.get_team_by_id(team_id, db)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team
