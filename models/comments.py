# Description: Comments model for the database
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from . import db

class Comment(db.Model, UserMixin):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50), nullable=False)

    # Foreign Key referencing UserDetails.id
    author_id = db.Column(db.Integer, db.ForeignKey("UserDetails.id"), nullable=False)
    comment_author = relationship("User", back_populates="comments")

    # Foreign Key referencing BlogPost.id
    post_id = db.Column(db.Integer, db.ForeignKey("BlogPost.id"), nullable=False)
    parent_post = relationship("BlogPost", back_populates="comments")



    def __repr__(self):
        return f'<Comment {self.text}>'