from flask import Flask
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_APP_KEY') or 'your-default-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///Agency.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True  # Set to False in production
