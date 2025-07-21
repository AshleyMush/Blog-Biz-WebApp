import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_APP_KEY', 'fallback-secret-key')

    # If DATABASE_URI is not set in environment, default to local SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or "sqlite:///BlogDataBase.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('FLASK_DEBUG', False)  # Use env var to toggle debug mode
    EMAIL_KEY = os.environ.get('EMAIL_KEY')
    PASSWORD_KEY = os.environ.get('PASSWORD_KEY')
