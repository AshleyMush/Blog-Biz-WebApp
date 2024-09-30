from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin


db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
    This class represents the User table.
    """
    __tablename__ = "UserDetails"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(nullable=False, default='User')  # Roles: 'Admin','Contributor',  'User'

    #-------- Relationship to blog posts
    posts = relationship("BlogPost", back_populates="author")

    def __repr__(self):
        """This method returns a string representation of the User object. for readability purposes."""
        return f"User('{self.email}', '{self.first_name}', '{self.last_name}')"

    # For api purposes, to convert the data to a dictionary
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class BlogPost(db.Model):
    __tablename__ = 'blog_post'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    subtitle: Mapped[str] = mapped_column(nullable=True)
    body: Mapped[str] = mapped_column(nullable=False)
    img_url: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[str] = mapped_column(nullable=False)


    # --- Relationship to the author
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"))
    # Create reference to the User object. The "posts" refers to the posts property in the User class.
    author = relationship("User", back_populates="posts")

    # Relationship to categories
    categories = db.relationship('Category', secondary=post_categories, backref=db.backref('posts', lazy='dynamic'))

    def __repr__(self):
        return f'<BlogPost {self.title}>'





class Services(db.Model):
    """
    This class represents the services table.
    """
    __tablename__ = "services"
    id: Mapped[int] = mapped_column(primary_key=True)
    service_name: Mapped[str] = mapped_column(nullable=True)
    homepage_description: Mapped[str] = mapped_column(nullable=True)  # Rich text content
    homepage_image_url: Mapped[str] = mapped_column(nullable=True)
    banner_subheading: Mapped[str] = mapped_column(nullable=True)
    feature_one_description: Mapped[str] = mapped_column(nullable=True)  # Rich text content
    feature_one_image_url: Mapped[str] = mapped_column(nullable=True)
    feature_two_description: Mapped[str] = mapped_column(nullable=True)  # Rich text content
    feature_two_image_url: Mapped[str] = mapped_column(nullable=True)



    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}















class HomePage(db.Model, UserMixin):
    __tablename__ = "home_page"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    heading: Mapped[str] = mapped_column(nullable=False)
    subheading: Mapped[str] = mapped_column(nullable=False)
    img_url: Mapped[str] = mapped_column(nullable=False)



    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class FAQs(db.Model, UserMixin):
    __tablename__ = "faqs"
    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(nullable=False)
    answer: Mapped[str] = mapped_column(nullable=False)


    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Inbox(db.Model, UserMixin):
    __tablename__ = "Inbox"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)


    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class ContactDetails(db.Model, UserMixin):
    __tablename__ = "contact_details"
    # Contact information
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    location: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(unique=True, nullable=True)
    facebook_url: Mapped[str] = mapped_column(nullable=True)
    instagram_url: Mapped[str] = mapped_column(nullable=True)
    twitter_url: Mapped[str] = mapped_column(nullable=True)


    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class ContactPageContent(db.Model, UserMixin):
    __tablename__ = "contact_page"
    id: Mapped[int] = mapped_column(primary_key=True)
    page_name: Mapped[str] = mapped_column(nullable=True)
    img_url: Mapped[str] = mapped_column(nullable=True)
    banner_subheading: Mapped[str] = mapped_column(nullable=True)
    content: Mapped[str] = mapped_column(nullable=True)  # Rich content
    img_one_url: Mapped[str] = mapped_column(nullable=True)
    description_one: Mapped[str] = mapped_column(nullable=True)  # Rich content
    img_two_url: Mapped[str] = mapped_column(nullable=True)
    description_two: Mapped[str] = mapped_column(nullable=True)  # Rich content
    img_three_url: Mapped[str] = mapped_column(nullable=True)
    description_three: Mapped[str] = mapped_column(nullable=True)  # Rich content



    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



class AboutPageContent(db.Model, UserMixin):
    __tablename__ = "about_page"
    id: Mapped[int] = mapped_column(primary_key=True)
    page_name: Mapped[str] = mapped_column(nullable=True)
    img_url: Mapped[str] = mapped_column(nullable=True)
    banner_subheading: Mapped[str] = mapped_column(nullable=True)
    content: Mapped[str] = mapped_column(nullable=True)  # Rich content
    img_one_url: Mapped[str] = mapped_column(nullable=True)
    description_one: Mapped[str] = mapped_column(nullable=True)  # Rich content
    img_two_url: Mapped[str] = mapped_column(nullable=True)
    description_two: Mapped[str] = mapped_column(nullable=True)  # Rich content
    img_three_url: Mapped[str] = mapped_column(nullable=True)
    description_three: Mapped[str] = mapped_column(nullable=True)  # Rich content

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Jobs(db.Model, UserMixin):
    __tablename__ = "Jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_name: Mapped[str] = mapped_column(nullable=False)
    job_card_img_url: Mapped[str] = mapped_column(nullable=False)
    job_description: Mapped[str] = mapped_column(nullable=False)
    # id = db.Column(db.Integer, primary_key=True)
    # job_name = db.Column(db.String(250), nullable=False)
    # job_card_img_url = db.Column(db.String(250), nullable=False)
    # job_description = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class CareerPageContent(db.Model, UserMixin):
    __tablename__ = "Career page content"
    id: Mapped[int] = mapped_column(primary_key=True)
    page_name: Mapped[str] = mapped_column(nullable=False)
    banner_heading: Mapped[str] = mapped_column(nullable=False)
    banner_subheading: Mapped[str] = mapped_column(nullable=False)
    page_content: Mapped[str] = mapped_column(nullable=False)  # Rich text content

    # id = db.Column(db.Integer, primary_key=True)
    # page_img_url = db.Column(db.String(250), nullable=False)
    # banner_heading = db.Column(db.String(250), nullable=False)
    # banner_subheading = db.Column(db.String(250), nullable=False)
    # page_content = db.Column(db.Text, nullable=False)  # Rich text content

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

