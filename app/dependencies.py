from fastapi import Depends
from sqlalchemy.orm import Session

from app import auth_utils, crud, schemas
from app.database import SessionLocal


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(auth_utils.oauth2_scheme),
) -> schemas.DBUser:
    email = auth_utils.decode_jwt(token)
    user = crud.get_user_auth(email, db)
    if user is None:
        raise auth_utils.credentials_exception
    return user
