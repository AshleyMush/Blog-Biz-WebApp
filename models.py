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
    
    # Service information
    service_name = db.Column(db.String(250), nullable=True)
    homepage_description = db.Column(db.Text, nullable=True)  # Rich text content
    
    # Images and banners for the service
    homepage_image_url = db.Column(db.String(250), nullable=True)
    banner_subheading = db.Column(db.String(250), nullable=True)
    
    # Feature descriptions and images
    feature_one_description = db.Column(db.Text, nullable=True)  # Rich text content
    feature_one_image_url = db.Column(db.String(250), nullable=True)
    feature_two_description = db.Column(db.Text, nullable=True)  # Rich text content
    feature_two_image_url = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}











class User(db.Model, UserMixin):
    """
    This class represents the User table.
    """
    __tablename__ = "UserDetails"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    number = db.Column(db.String(250), nullable=True)
    role = db.Column(db.String(50), nullable=False, default='User')  # Roles: 'Admin','Contributor','Moderator' ,  'User'


    def __repr__(self):
        """This method returns a string representation of the User object. for readability purposes."""
        return f"User('{self.email}', '{self.first_name}', '{self.last_name}')"


    # For api purposes, to convert the data to a dictionary
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



class HomePage(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    heading = db.Column(db.String(250), unique=True, nullable=False)
    subheading = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class FAQs(db.Model, UserMixin):
    __tablename__ = "faqs"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(250), nullable=False)
    answer = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Inbox(db.Model, UserMixin):
    __tablename__ = "Inbox"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    number = db.Column(db.String(250), nullable=True)
    email = db.Column(db.String(250), nullable=True)
    message = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class ContactDetails(db.Model, UserMixin):
    __tablename__ = "contact_details"
    # Contact information
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=True)
    location = db.Column(db.Text, nullable=True)
    phone_number = db.Column(db.String(250), unique=True, nullable=True)
    facebook_url = db.Column(db.String(250), nullable=True)
    instagram_url = db.Column(db.String(250), nullable=True)
    twitter_url = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class ContactPageContent(db.Model, UserMixin):
    __tablename__ = "contact_page"
    id = db.Column(db.Integer, primary_key=True)
    # Contact Page data
    page_name = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=True)
    banner_subheading = db.Column(db.String(250), nullable=True)
    content = db.Column(db.Text, nullable=True) # Rich content
    img_one_url = db.Column(db.String(250), nullable=True)
    description_one = db.Column(db.Text, nullable=True) # Rich content
    img_two_url = db.Column(db.String(250), nullable=True)
    description_two = db.Column(db.Text, nullable=True) # Rich content
    img_three_url = db.Column(db.String(250), nullable=True)
    description_three = db.Column(db.Text, nullable=True) # Rich content

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



class AboutPageContent(db.Model, UserMixin):
    __tablename__ = "about_page"
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(250), nullable=False)
    banner_subheading = db.Column(db.String(250), nullable=False)
    feature_one_description = db.Column(db.Text, nullable=False)  # Rich text content
    feature_one_image_url = db.Column(db.String(250), nullable=False)
    feature_two_description = db.Column(db.Text, nullable=False)  # Rich text content
    feature_two_image_url = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Jobs(db.Model, UserMixin):
    __tablename__ = "Jobs"
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(250), nullable=False)
    job_card_img_url = db.Column(db.String(250), nullable=False)
    job_description = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class CareerPageContent(db.Model, UserMixin):
    __tablename__ = "Career page content"

    id = db.Column(db.Integer, primary_key=True)
    page_img_url = db.Column(db.String(250), nullable=False)
    banner_heading = db.Column(db.String(250), nullable=False)
    banner_subheading = db.Column(db.String(250), nullable=False)
    page_content = db.Column(db.Text, nullable=False)  # Rich text content

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

