import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///release_date_hub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'c006e7558c35ca45378686fd800fafa0'
app.secret_key = 'SECRET KEY'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='mrsnoogi@gmail.com',
    MAIL_PASSWORD='LaurelGillis1'
)
mail = Mail(app)

from releasedatehub.users.routes import users
from releasedatehub.items.routes import items
from releasedatehub.main.routes import main
app.register_blueprint(users)
app.register_blueprint(items)
app.register_blueprint(main)

