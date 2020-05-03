from flask import Flask, render_template, request, redirect, session, url_for, flash
from forms import RegistrationForm, LoginForm
from newsapi import NewsApiClient
from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate

import re
import os
from pathlib import Path
from dateutil.parser import parse

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///release_date_hub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# do i need both secret keys?
app.config['SECRET_KEY'] = 'c006e7558c35ca45378686fd800fafa0'
app.secret_key = 'SECRET KEY'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

# news api ( consider moveing api to another module )
newsapi = NewsApiClient(api_key='571610756dbb460298a1abbe29199de9')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'))
    author = db.relationship('User', foreign_keys=[author_id], backref='user_itemsaa')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=pw_hash)
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(username=form.username.data).first()
        session['userid'] = user.id
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if bcrypt.check_password_hash(user.password, form.password.data):
            session['userid'] = user.id
            flash('You have logged in', 'success')
            return redirect(url_for('dashboard'))
    return render_template('login.html', title='Log In', form=form)

@app.route('/on_logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/on_add_item', methods=['POST'])
def on_add_item():
    
    if request.form['date']:
        print('date found')
        python_date = parse(request.form['date'])
        item = Item(name=request.form['name'], date = python_date, author_id = session['userid'])
        db.session.add(item)
        db.session.commit()
        print('finished date found statement')

    else:
        print('no date found')
        item = Item(name=request.form['name'], author_id=session['userid'])
        db.session.add(item)
        db.session.commit()
        print('finished no date statement')
    
    return redirect('/dashboard')

@app.route('/on_delete/<id>', methods=['POST', 'GET'])
def on_delete(id):
    item = Item(id=id)
    db.session.remove(item)
    db.session.commit()
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    items = Item.query.filter_by(author_id=session['userid'])
    if items:
        return render_template('dashboard.html', items=items, title='Dashboard')
    else:
        return render_template('dashboard.html', title='Dashboard')
    # add news article notification logic

@app.route('/item/<title>')
def item(title):

    news = newsapi.get_everything(q=f'{title} release', language='en')
    
    articles = news['articles']

    # for i in articles:
    #     print(i['urlToImage'])
    #     print(i['title'])
    #     print(i['author'])
    #     print(i['description'])
    #     print(i['url'])
    #     print(i['publishedAt'])
    #     print('*'*50)

    # for key, value in articles[0].items():
    #     print(f"\n{key.ljust(15)} {value}")

    return render_template('item.html', articles=articles, title=title)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/edit/<id>')
def edit(id):
    return 'yup'

if __name__ == "__main__":
    app.run(debug=True)