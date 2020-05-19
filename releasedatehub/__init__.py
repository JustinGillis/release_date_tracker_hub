from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bcrypt import Bcrypt 
from releasedatehub.config import Config
from newsapi import NewsApiClient

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
newsapi = NewsApiClient(api_key=Config.NEWSAPI_KEY)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    from releasedatehub.users.routes import users
    from releasedatehub.items.routes import items
    from releasedatehub.main.routes import main
    from releasedatehub.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(items)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
    