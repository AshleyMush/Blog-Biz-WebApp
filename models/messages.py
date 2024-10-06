# Description: Comments model for the database
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from . import db

class Message(db.Model, UserMixin):
    __tablename__ = "messages"
    id : Mapped[int] = mapped_column(primary_key=True)
    text : Mapped[str] = mapped_column(nullable=False)
    date : Mapped[str] = mapped_column(nullable=False)

    # Foreign Key referencing UserDetails.id
    author_id = db.Column(db.Integer, db.ForeignKey("UserDetails.id"))
    message_author = relationship("User", back_populates="messages")

    def __repr__(self):
        return f'<Comment {self.text}>'