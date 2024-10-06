# models/__init__.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User, Inbox
from .blog import BlogPost, DraftPost, Category, post_categories
from.comments import Comment
from.bmi_entry import BMIEntry
from.messages import Message
from .business import (
    HomePage,
    FAQs,
    Services,
    AboutPageContent,
    ContactPageContent,
    ContactDetails,
    CareerPageContent
)
