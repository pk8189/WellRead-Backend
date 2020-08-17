from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from app import crud, schemas


class User:
    def __init__(self, db: Session, user: schemas.User = None):
        self.db = db
        self.user = user

    def email_not_in_use(self, email: str) -> bool:
        db_user = crud.get_user_by_email(email, self.db)
        if db_user is not None:
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )


class Club:
    def __init__(self, db: Session, user: schemas.User, id: int):
        self.id = id
        self.db = db
        self.user = user

    def read(self) -> schemas.Club:
        db_club = crud.read_club(self.user.id, self.id, self.db)
        if db_club is None:
            raise HTTPException(status_code=400, detail="Club not found")
        return db_club

    def exists(self) -> bool:
        self.read()
        return True

    def is_admin(self) -> bool:
        db_club = self.read()
        if db_club.admin_user_id != self.user.id:
            raise HTTPException(
                status_code=403, detail="Unauthorized, user is not club admin",
            )
        return True

    def is_invited(self) -> bool:
        club_for_joining = crud.read_clubs_for_joining(self.id, self.db)
        if club_for_joining is None:
            raise HTTPException(status_code=400, detail="Club not found")
        return True

    def duplicate_tag(self, name: str) -> bool:
        self.read()
        duplicate_tag = crud.read_duplicate_tag(self.id, name, self.db,)
        if duplicate_tag:
            raise HTTPException(
                status_code=400, detail="Tag with this name already exists"
            )


class Book:
    def __init__(self, db: Session, user: schemas.User, id: int):
        self.id = id
        self.db = db
        self.user = user

    def read(self) -> schemas.Note:
        db_book = crud.read_book(self.user.id, self.id, self.db)
        if db_book is None:
            raise HTTPException(status_code=400, detail="Book not found")
        return db_book

    def is_admin(self) -> bool:
        db_book = self.read()
        if db_book.club.admin_user_id != self.user.id:
            raise HTTPException(
                status_code=403, detail="Unauthorized, user is not club admin",
            )


class Note:
    def __init__(self, db: Session, user: schemas.User, id: int):
        self.id = id
        self.db = db
        self.user = user

    def read(self) -> schemas.Note:
        db_note = crud.read_note(self.user.id, self.id, self.db)
        if db_note is None:
            raise HTTPException(status_code=400, detail="Note not found")
        return db_note

    def can_read(self) -> bool:
        db_note = self.read()
        is_owner = db_note.user_id == self.user.id
        is_private = db_note.private
        if not is_owner and is_private:
            raise HTTPException(
                status_code=403,
                detail="Unauthorized, user is not owner of private note",
            )
        return True

    def can_update(self) -> bool:
        db_note = self.read()
        is_owner = db_note.user_id == self.user.id
        if not is_owner:
            raise HTTPException(
                status_code=403, detail="Unauthorized, user is not owner of note",
            )
        return True

    def can_delete(self) -> bool:
        return self.can_update()


class Tag:
    def __init__(self, db: Session, user: schemas.User, id: int):
        self.id = id
        self.db = db
        self.user = user

    def read(self) -> schemas.Tag:
        db_tag = crud.read_tag(self.user.id, self.id, self.db)
        if db_tag is None:
            raise HTTPException(status_code=400, detail="Tag not found")
        return db_tag

    def can_read(self) -> bool:
        db_tag = self.read()
        db_club = crud.read_club(self.user.id, db_tag.club_id, self.db)
        if db_club is None:
            raise HTTPException(status_code=400, detail="Club not found")
        return True

    def is_admin(self) -> bool:
        db_tag = self.read()
        if db_tag.club.admin_user_id != self.user.id:
            raise HTTPException(
                status_code=403, detail="Unauthorized, user is not club admin",
            )
