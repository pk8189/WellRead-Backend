import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.database import Base, WellReadBase

slack_club_slack_user_table = Table(
    "slack_club_slack_user",
    Base.metadata,
    Column(
        "slack_user_slack_id_team_id",
        String,
        ForeignKey("slack_users.slack_id_team_id"),
    ),
    Column("slack_club_id", Integer, ForeignKey("slack_clubs.id")),
)


class SlackTeam(Base, WellReadBase):
    __tablename__ = "slack_teams"

    team_id = Column(String, primary_key=True, index=True)  # team_id from slack API
    name = Column(String)  # team name from slack API team object
    domain = Column(String, nullable=True)  # domain from slack API team object
    email_domain = Column(String, nullable=True)  # email from slack API team object

    slack_users = relationship("SlackUser", back_populates="slack_team")


class SlackUser(Base, WellReadBase):
    __tablename__ = "slack_users"

    slack_id_team_id = Column(
        String, primary_key=True, index=True
    )  # user_id_team_id from slack API
    name = Column(String)  # full name given in user object of slack API
    tz = Column(String)
    locale = Column(String)  # chosen IETF language code for user

    team_id = Column(String, ForeignKey("slack_teams.team_id"), nullable=False)

    slack_team = relationship("SlackTeam", back_populates="slack_users")
    slack_clubs = relationship(
        "SlackClub", secondary=slack_club_slack_user_table, back_populates="slack_users"
    )
    notes = relationship("Note", back_populates="slack_user")


class SlackClub(Base, WellReadBase):
    __tablename__ = "slack_clubs"

    id = Column(Integer, primary_key=True, index=True)
    book_title = Column(String)
    channel_id = Column(String)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    intro_message_ts = Column(String, nullable=True)

    admin_user_id = Column(String, ForeignKey("slack_users.slack_id_team_id"))

    slack_users = relationship(
        "SlackUser", secondary=slack_club_slack_user_table, back_populates="slack_clubs"
    )
    notes = relationship("Note", back_populates="slack_club", cascade="all, delete")
    tags = relationship("Tag", back_populates="slack_club", cascade="all, delete")


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

    slack_user_id = Column(String, ForeignKey("slack_users.slack_id_team_id"))
    slack_club_id = Column(Integer, ForeignKey("slack_clubs.id"))

    slack_user = relationship("SlackUser", back_populates="notes")
    slack_club = relationship("SlackClub", back_populates="notes")
    tags = relationship("Tag", secondary=note_tag_table, back_populates="notes")


class Tag(Base, WellReadBase):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    archived = Column(Boolean, default=False)

    slack_club_id = Column(Integer, ForeignKey("slack_clubs.id"))

    slack_club = relationship("SlackClub", back_populates="tags")
    notes = relationship("Note", secondary=note_tag_table, back_populates="tags")
