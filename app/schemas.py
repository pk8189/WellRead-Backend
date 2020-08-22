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


class BookBase(BaseModel):
    id: int
    book_title: str
    author_name: str

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


class NoteBase(BaseModel):
    id: int
    create_date: datetime
    content: str
    private: bool
    archived: bool
    user_id: int
    book_id: int

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    id: int
    name: str
    create_date: datetime
    archived: bool
    user_id: int

    class Config:
        orm_mode = True


class ClubTagBase(BaseModel):
    id: int
    name: str
    create_date: datetime
    archived: bool
    book_id: int
    club_id: int

    class Config:
        orm_mode = True


# User schemas
class UserFollow(BaseModel):
    id: int
    full_name: str


class User(UserBase):
    books: List[BookBase]
    tags: List[TagBase]
    clubs: List[ClubBase]
    notes: List[NoteBase]
    following: List[UserBase]
    followers: List[UserBase]


class DBUser(UserBase):
    hashed_password: str


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str


# Book schemas
class Book(BookBase):
    tags: List[TagBase]
    clubs: List[ClubBase]
    users: List[UserBase]
    notes: List[NoteBase]
    club_tags: List[ClubTagBase]


class BookCreate(BaseModel):
    book_title: str
    author_name: str


class BookUpdate(BaseModel):
    book_title: Optional[str] = None
    author_name: Optional[str] = None
    archived: Optional[bool] = None


class BookDelete(BookBase):
    pass


# Club schemas
class Club(ClubBase):
    users: List[UserBase]
    club_tags: List[ClubTagBase]
    books: List[BookBase]


class Clubs(BaseModel):
    clubs: List[Club]


class ClubCreate(BaseModel):
    name: str
    # admin_user_id comes from token


class ClubUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    current_book: Optional[bool] = None


class ClubDelete(ClubBase):
    pass


# Note schemas
class Note(NoteBase):
    tags: List[TagBase]
    club_tags: List[ClubTagBase]


class Notes(BaseModel):
    notes: List[Note]


class NoteCreate(BaseModel):
    content: str
    book_id: int
    private: Optional[bool]


class NoteUpdate(BaseModel):
    content: str
    private: Optional[bool]
    archived: Optional[bool]


class NoteAddTagsAndClubTags(BaseModel):
    tags: List[int]
    club_tags: List[int]


class NoteDelete(NoteBase):
    pass


# Tag schemas
class Tag(TagBase):
    books: List[BookBase]
    notes: List[NoteBase]


class Tags(BaseModel):
    tags: List[Tag]


class TagCreate(BaseModel):
    name: str


class TagUpdate(BaseModel):
    name: str
    archived: bool


class TagDelete(TagBase):
    pass


class ClubTag(ClubTagBase):
    notes: List[NoteBase]


class ClubTags(BaseModel):
    club_tags: List[ClubTag]


class ClubTagCreate(BaseModel):
    name: str
    book_id: int
    club_id: int


class ClubTagUpdate(BaseModel):
    name: str
    archived: bool


class ClubTagDelete(ClubTagBase):
    pass
