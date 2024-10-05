# Description: Comments model for the database
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from . import db

class Message(db.Model, UserMixin):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50), nullable=False)

    # Foreign Key referencing UserDetails.id
    author_id = db.Column(db.Integer, db.ForeignKey("UserDetails.id"))
    message_author = relationship("User", back_populates="messages")

    def __repr__(self):
        return f'<Comment {self.text}>'