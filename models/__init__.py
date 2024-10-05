# models/__init__.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User, Inbox
from .blog import BlogPost
from.comments import Comment
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
