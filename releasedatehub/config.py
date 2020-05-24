import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///release_date_hub.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'c006e7558c35ca45378686fd800fafa0aa'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'release.date.hub@gmail.com'
    MAIL_PASSWORD = 'Gp2js8!30'
    NEWSAPI_KEY = '571610756dbb460298a1abbe29199de9'
    



