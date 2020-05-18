from flask import render_template, request, redirect, session, url_for, flash, abort

from releasedatehub import app, db, mail
from releasedatehub.forms import RegistrationForm, LoginForm, UpdateAccountForm, ItemForm, RequestResetForm, ResetPasswordForm
from releasedatehub.models import User, Item
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
 
import re
from newsapi import NewsApiClient
from flask_bcrypt import Bcrypt 
from dateutil.parser import parse

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)
newsapi = NewsApiClient(api_key='571610756dbb460298a1abbe29199de9')