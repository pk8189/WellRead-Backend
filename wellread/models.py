import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from wellread.database import Base, WellReadBase

slack_club_slack_user_table = Table(
    "slack_club_slack_user",
    Base.metadata,
    Column(
        "slack_user_slack_id_team_id",
        String,
        ForeignKey("slack_users.slack_id_team_id"),
    ),
    Column("slack_club_id", String, ForeignKey("slack_clubs.id")),
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
    email = Column(String)  # email from slack API user object
    name = Column(String)  # full name given in user object of slack API
    is_app_user = Column(Boolean)  # user is authorized to call our app
    is_owner = Column(Boolean)  # user is an owner of the current workspace
    locale = Column(String)  # chosen IETF language code for user
    profile_image_original = Column(String)  # profile image URL

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
    next_meeting = Column(DateTime, nullable=True)

    admin_user_id = Column(String, ForeignKey("slack_users.slack_id_team_id"))
    slack_users = relationship(
        "SlackUser", secondary=slack_club_slack_user_table, back_populates="slack_clubs"
    )
    notes = relationship("Note", back_populates="slack_club")


class Note(Base, WellReadBase):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(String, index=True)

    slack_user_id = Column(String, ForeignKey("slack_users.slack_id_team_id"))
    slack_club_id = Column(Integer, ForeignKey("slack_clubs.id"))
    slack_user = relationship("SlackUser", back_populates="notes")
    slack_club = relationship("SlackClub", back_populates="notes")


# tags = relationship("TagNotesAssociation", back_populates="tags")


# class TagNotesAssociation(Base, WellReadBase):
#     __tablename__ = "tags_notes_association"

#     tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)
#     note_id = Column(Integer, ForeignKey("note.id"), primary_key=True)
#     tag = relationship("Tag", back_populates="notes")
#     note = relationship("Note", back_populates="tags")

# class Tag(Base, WellReadBase):
#     __tablename__ = "tags"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)

#     created_by = Column(Integer, ForeignKey("users.id"))
#     owner = relationship("User", back_populates="items")

#     notes = relationship("TagNotesAssociation", back_populates="notes")
