from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///release_date_hub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# do i need both secret keys?
app.config['SECRET_KEY'] = 'c006e7558c35ca45378686fd800fafa0'
app.secret_key = 'SECRET KEY'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

from releasedatehub import routes


