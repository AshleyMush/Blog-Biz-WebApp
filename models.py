from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin


db = SQLAlchemy()


class Services(db.Model):
    """
    This class represents the services table.
    """
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(250), nullable=False)
    homepage_img_url = db.Column(db.String(250), nullable=False)
    homepage_content = db.Column(db.Text, nullable=False)  # Rich text content
    servicepage_img_url = db.Column(db.String(250), nullable=False)
    banner_subheading = db.Column(db.String(250), nullable=False)
    body_content = db.Column(db.Text, nullable=False)  # Rich text content

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}







class User(db.Model, UserMixin):
    """
    This class represents the User table.
    """
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



class HomePage(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    heading = db.Column(db.String(250), unique=True, nullable=False)
    subheading = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class FAQs(db.Model, UserMixin):
    __tablename__ = "faqs"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(250), nullable=False)
    answer = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Contacts(db.Model, UserMixin):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    location = db.Column(db.Text, nullable=False)
    phone_number = db.Column(db.String(250), unique=True, nullable=False)
    facebook_url = db.Column(db.String(250), nullable=True)
    instagram_url = db.Column(db.String(250), nullable=True)
    twitter_url = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class AboutUs(db.Model, UserMixin):
    __tablename__ = "about_us"
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(250), nullable=False)
    banner_heading = db.Column(db.String(250), nullable=False)
    banner_subheading = db.Column(db.String(250), nullable=False)
    banner_content = db.Column(db.Text, nullable=False)  # Rich text content

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class JoinUs(db.Model, UserMixin):
    __tablename__ = "join_us"
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(250), nullable=False)
    banner_heading = db.Column(db.String(250), nullable=False)
    banner_subheading = db.Column(db.String(250), nullable=False)
    banner_content = db.Column(db.Text, nullable=False)  # Rich text content
    job_card_heading = db.Column(db.String(250), nullable=False)
    job_card_img_url = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

