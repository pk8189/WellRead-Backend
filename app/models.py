import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app import associations
from app.database import Base, WellReadBase


class User(Base, WellReadBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    books = relationship(
        "Book", back_populates="users", secondary=associations.books_users
    )
    clubs = relationship(
        "Club", back_populates="users", secondary=associations.clubs_users
    )
    tags = relationship("Tag", back_populates="user_id")
    notes = relationship("Note", back_populates="user_id")


class Book(Base, WellReadBase):
    """
    https://www.isbndb.com/apidocs/v2 should eventually as way to
    search / refer to books (isbn at primary key)
    """

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    book_title = Column(String, nullable=False)
    author_name = Column(String, nullable=False)

    tags = relationship(
        "Tag", back_populates="books", secondary=associations.books_tags
    )
    clubs = relationship(
        "Club", back_populates="books", secondary=associations.books_clubs
    )
    users = relationship(
        "User", back_populates="books", secondary=associations.books_users
    )
    notes = relationship("Note", back_populates="book")
    club_tags = relationship("ClubTag", back_populates="book")


class Club(Base, WellReadBase):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    current_book = Column(Integer, ForeignKey("books.id"))

    admin_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    users = relationship(
        "User", back_populates="clubs", secondary=associations.clubs_users
    )
    books = relationship(
        "Book", back_populates="clubs", secondary=associations.books_clubs
    )
    club_tags = relationship("ClubTag", back_populates="club")


class Note(Base, WellReadBase):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(String, index=True, nullable=False)
    private = Column(Boolean, default=False, nullable=False)
    archived = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="notes")
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    book = relationship("Book", back_populates="notes")

    tags = relationship(
        "Tag", back_populates="notes", secondary=associations.notes_tags
    )
    club_tags = relationship(
        "Club_Tag", back_populates="notes", secondary=associations.club_tags_notes
    )


class Tag(Base, WellReadBase):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    archived = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="tags")

    books = relationship(
        "Book", back_populates="tags", secondary=associations.books_tags
    )
    notes = relationship(
        "Note", back_populates="tags", secondary=associations.notes_tags
    )


class ClubTag(Base, WellReadBase):
    __tablename__ = "club_tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    archived = Column(Boolean, default=False)

    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    book = relationship("Book", back_populates="club_tags")
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)
    club = relationship("Club", back_populates="club_tags")

    notes = relationship(
        "Note", back_populates="club_tags", secondary=associations.club_tags_notes
    )
