import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.database import Base, WellReadBase

club_user_table = Table(
    "club_user_table",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"),),
    Column("club_id", Integer, ForeignKey("clubs.id")),
)


class User(Base, WellReadBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String)
    hashed_password = Column(String)

    clubs = relationship("Club", secondary=club_user_table, back_populates="users")
    notes = relationship("Note", back_populates="user")


class Club(Base, WellReadBase):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)

    admin_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    users = relationship("User", secondary=club_user_table, back_populates="clubs")
    books = relationship("Book", back_populates="club", cascade="all, delete")
    notes = relationship("Note", back_populates="club", cascade="all, delete")
    tags = relationship("Tag", back_populates="club", cascade="all, delete")


class Book(Base, WellReadBase):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    book_title = Column(String, nullable=False)
    author_name = Column(String, nullable=False)
    archived = Column(Boolean, default=False)

    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)

    club = relationship("Club", back_populates="books")


note_tag_table = Table(
    "note_tag",
    Base.metadata,
    Column("note_tag", Integer, ForeignKey("notes.id"),),
    Column("tag", Integer, ForeignKey("tags.id")),
)


class Note(Base, WellReadBase):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(String, index=True)
    private = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    club_id = Column(Integer, ForeignKey("clubs.id"))

    user = relationship("User", back_populates="notes")
    club = relationship("Club", back_populates="notes")
    tags = relationship("Tag", secondary=note_tag_table, back_populates="notes")


class Tag(Base, WellReadBase):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    archived = Column(Boolean, default=False)

    club_id = Column(Integer, ForeignKey("clubs.id"))

    club = relationship("Club", back_populates="tags")
    notes = relationship("Note", secondary=note_tag_table, back_populates="tags")
