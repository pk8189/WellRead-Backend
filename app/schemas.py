from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class Token(BaseModel):
    access_token: str
    token_type: str


# Base models which map to the sqlalchemy ORM


class UserBase(BaseModel):
    id: int
    full_name: str
    email: str

    class Config:
        orm_mode = True


class ClubBase(BaseModel):
    id: int
    name: str
    create_date: datetime
    is_active: bool
    admin_user_id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    id: int
    book_title: str
    author_name: str
    archived: bool
    club_id: int

    class Config:
        orm_mode = True


class NoteBase(BaseModel):
    id: int
    create_date: datetime
    content: str
    user_id: int
    club_id: int
    private: bool
    archived: bool

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    id: int
    name: str
    create_date: datetime
    archived: bool
    club_id: int

    class Config:
        orm_mode = True


# Tag schemas
class TagCreate(BaseModel):
    name: str
    club_id: int


class TagUpdate(BaseModel):
    name: str
    archived: bool


class TagDelete(TagBase):
    pass


# Note schemas
class NoteCreate(BaseModel):
    content: str
    club_id: int
    private: Optional[bool]


class NoteUpdate(BaseModel):
    content: str
    private: Optional[bool]
    archived: Optional[bool]


class NoteAddTags(BaseModel):
    tags: List[int]


class NoteDelete(NoteBase):
    pass


# Club schemas
class ClubCreate(BaseModel):
    name: str


class ClubUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    current_book_id: Optional[bool] = None


class ClubDelete(ClubBase):
    pass


class BookCreate(BaseModel):
    book_title: str
    author_name: str
    club_id: int


class BookUpdate(BaseModel):
    book_title: Optional[str] = None
    author_name: Optional[str] = None
    archived: Optional[bool] = None


class BookDelete(BookBase):
    pass


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str


class DBUser(UserBase):
    hashed_password: str


class User(UserBase):
    clubs: List[ClubBase]
    notes: List[NoteBase]


class Club(ClubBase):
    users: List[UserBase]
    tags: List[TagBase]
    books: List[BookBase]


class Clubs(BaseModel):
    clubs: List[Club]


class Book(BookBase):
    club: ClubBase


class Note(NoteBase):
    tags: List[TagBase]
    user: UserBase
    club: ClubBase


class Notes(BaseModel):
    notes: List[Note]


class Tag(TagBase):
    club: ClubBase
    notes: List[NoteBase]


class Tags(BaseModel):
    tags: List[Tag]
