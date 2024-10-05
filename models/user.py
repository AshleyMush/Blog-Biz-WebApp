# models/user.py

from flask_login import UserMixin
from sqlalchemy.orm import relationship
from . import db

class User(db.Model, UserMixin):
    __tablename__ = "UserDetails"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(50), nullable=False, default='User')  # Roles: 'Admin','Contributor','User'

    #---- Relationships
    posts = relationship("BlogPost", back_populates="author")
    drafts = relationship("DraftPost", back_populates="author")
    #"comment_author" refers to the comment_author property in the Comment class.
    comments = relationship("Comment", back_populates="comment_author")
    messages = relationship("Message", back_populates="message_author")

    def __repr__(self):
        return f'<User {self.email}>'


class Inbox(db.Model, UserMixin):
    __tablename__ = "Inbox"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Inbox {self.email}>'
