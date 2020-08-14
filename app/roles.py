from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud


def club_exists_and_is_admin(user_id: int, club_id: int, db: Session) -> bool:
    db_club = crud.read_club(user_id, club_id, db)
    if db_club is None:
        raise HTTPException(status_code=400, detail="Club not found")
    if db_club.admin_user_id != user_id:
        raise HTTPException(
            status_code=403, detail="Unauthorized, user is not club admin",
        )
    return True
