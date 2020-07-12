from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Time

from wellread.database import Base


class SlackTeam(Base):
    __tablename__ = "slack_teams"

    team_id = Column(String, primary_key=True, index=True)  # team_id from slack API
    name = Column(String)  # team name from slack API team object
    domain = Column(String)  # domain from slack API team object
    email_domain = Column(String)  # email from slack API team object


# class SlackUser(Base):
#     __tablename__ = "slack_users"

#     slack_id = Column(String, primary_key=True, index=True) # user_id + team_id from slack API
#     email = Column(String) # email from slack API user object
#     name = Column(String) # full name given in user object of slack API
#     is_app_user = Column(Boolean) # user is authorized to call our app
#     is_owner = Column(Boolean) # user is an owner of the current workspace
#     locale = Column(String) # chosen IETF language code for user
#     profile_image_original = Column(String) # profile image URL


# slack_club = relationship(
#     "SlackClub",
#     secondary=slack_club_slack_user_table,
#     back_populates="slack_users"
# )


# slack_club_slack_user_table = Table("slack_club_slack_user", Base.metadata,
#     Column("slack_club_id", Integer, ForeignKey("slack_clubs.id")),
#     Column("slack_user_id", Integer, ForeignKey("slack_users.id"))
# )


# class SlackClub(Base):
#     __tablename__ = "slack_clubs"

#     id = Column(Integer, primary_key=True, index=True)
#     created = Column(Time)
#     book_title = Column(String)
#     next_meeting = Column(Time)
#     is_active = Column(Boolean)
#     workspace_id = Column(String)
#     channel_id = Column(String)

#     #admin_user_id = ForeignKey("slack_user.id")
#     slack_user = relationship(
#         "SlackUser",
#         secondary=slack_club_slack_user_table,
#         backref="slack_clubs"
#     )


# class Note(Base):
#     __tablename__ = "notes"

#     id = Column(Integer, primary_key=True, index=True)
#     ts = Column(Time, index=True)
#     content = Column(String, index=True)

#     user = relationship("User", back_populates="notes")
# tags = relationship("TagNotesAssociation", back_populates="tags")


# class TagNotesAssociation(Base):
#     __tablename__ = "tags_notes_association"

#     tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)
#     note_id = Column(Integer, ForeignKey("note.id"), primary_key=True)
#     tag = relationship("Tag", back_populates="notes")
#     note = relationship("Note", back_populates="tags")

# class Tag(Base):
#     __tablename__ = "tags"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)

#     created_by = Column(Integer, ForeignKey("users.id"))
#     owner = relationship("User", back_populates="items")

#     notes = relationship("TagNotesAssociation", back_populates="notes")
