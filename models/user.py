# models/user.py

from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from . import db

class User(db.Model, UserMixin):
    __tablename__ = "UserDetails"
    id : Mapped[int] = mapped_column(primary_key=True)
    email : Mapped[str] = mapped_column(nullable=False)
    password : Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name : Mapped[str] = mapped_column(nullable=False)
    phone_number : Mapped[str] = mapped_column(nullable=True)
    about : Mapped[str] = mapped_column(nullable=True)
    role : Mapped[str] = mapped_column(nullable=False, default='User') # Roles: 'Admin','Contributor','User'

    #---- Relationships
    posts = relationship("BlogPost", back_populates="author")
    drafts = relationship("DraftPost", back_populates="author")
    #"comment_author" refers to the comment_author property in the Comment class.
    comments = relationship("Comment", back_populates="comment_author")
    messages = relationship("Message", back_populates="message_author")

    # Relationship to BMIEntries
    bmi_entries = relationship("BMIEntry", back_populates="user", cascade="all, delete-orphan")


    def __repr__(self):
        return f'<User {self.email}>'


class Inbox(db.Model, UserMixin):
    __tablename__ = "Inbox"
    id: Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(nullable=False)
    email  : Mapped[str] = mapped_column(nullable=False)
    subject : Mapped[str] = mapped_column(nullable=False, unique=False)
    message : Mapped[str] = mapped_column(nullable=False, unique=False)
    date : Mapped[str] = mapped_column(nullable=False, unique=False)

    def __repr__(self):
        return f'<Inbox {self.email}>'
