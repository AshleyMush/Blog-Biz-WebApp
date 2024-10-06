# models/blog.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin

from . import db

# Association Table for BlogPost and Category (many-to-many relationship)
post_categories = Table(
    'post_categories',
    db.Model.metadata,
    db.Column('post_id', db.Integer, ForeignKey('BlogPost.id'), primary_key=True),
    db.Column('category_id', db.Integer, ForeignKey('Category.id'), primary_key=True)
)

class DraftPost(db.Model):
    __tablename__ = 'drafts'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    subtitle: Mapped[str] = mapped_column(nullable=True)
    body: Mapped[str] = mapped_column(nullable=False)
    img_url: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[str] = mapped_column(nullable=False)
    recommended: Mapped[bool] = mapped_column(nullable=False, default=False)  # New field


    # Foreign Key referencing UserDetails.id
    author_id: Mapped[int] = mapped_column(ForeignKey("UserDetails.id"))
    author = relationship("User", back_populates="drafts")

    def __repr__(self):
        return f'<DraftPost {self.title}>'

    # For API purposes, to convert the data to a dictionary
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class BlogPost(db.Model):
    __tablename__ = 'BlogPost'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    subtitle: Mapped[str] = mapped_column(nullable=True)
    body: Mapped[str] = mapped_column(nullable=False)
    img_url: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[str] = mapped_column(nullable=False)


    # Foreign Key referencing UserDetails.id
    author_id: Mapped[int] = mapped_column(ForeignKey("UserDetails.id"), nullable=False)
    author = relationship("User", back_populates="posts")

    # Relationship to Comment
    comments = relationship("Comment", back_populates="parent_post", cascade="all, delete-orphan")

    # Many-to-Many relationship with Category
    categories = relationship("Category", secondary=post_categories, back_populates="posts")

    def __repr__(self):
        return f'<BlogPost {self.title[:20]}...>'

    # For API purposes, to convert the data to a dictionary
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Category(db.Model):
    __tablename__ = 'Category'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    # Many-to-Many relationship with BlogPost
    posts = relationship("BlogPost", secondary=post_categories, back_populates="categories")

    def __repr__(self):
        return f'<Category {self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
