import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///release_date_hub.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY')
    



