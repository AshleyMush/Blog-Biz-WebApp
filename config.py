from flask import Flask
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_APP_KEY')
    SQLALCHEMY_DATABASE_URI =  os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False  # Set to False in production
    EMAIL_KEY = os.environ.get('EMAIL_KEY')
    PASSWORD_KEY = os.environ.get('PASSWORD_KEY')
