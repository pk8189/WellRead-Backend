from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database import Base

user_following = Table(
    "user_following",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("following_id", Integer, ForeignKey("users.id"), primary_key=True),
)

books_users = Table(
    "books_users",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"),),
    Column("user_id", Integer, ForeignKey("users.id")),
)

clubs_users = Table(
    "clubs_users",
    Base.metadata,
    Column("club_id", Integer, ForeignKey("clubs.id"),),
    Column("user_id", Integer, ForeignKey("users.id")),
)

books_tags = Table(
    "books_tags",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"),),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)

books_clubs = Table(
    "books_clubs",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"),),
    Column("club_id", Integer, ForeignKey("clubs.id")),
)

notes_tags = Table(
    "notes_tags",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id"),),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)

club_tags_notes = Table(
    "club_tags_notes",
    Base.metadata,
    Column("club_tag_id", Integer, ForeignKey("club_tags.id"),),
    Column("note_id", Integer, ForeignKey("notes.id")),
)
