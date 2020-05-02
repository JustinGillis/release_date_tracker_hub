from flask import Flask, render_template, request, redirect, session
from newsapi import NewsApiClient
import re
from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
import os
from pathlib import Path
from dateutil.parser import parse

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///release_date_hub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = 'secret key'
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
def index():
    return render_template('index.html')

@app.route('/on_register', methods=['POST'])
def on_register():
    is_valid = True
    if is_valid:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        new_user = User(username=request.form['username'], email=request.form['email'], password=pw_hash)
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(username=request.form['username']).first()
        session['userid'] = user.id
        return redirect('/dashboard')
    else:
        return redirect('/')

@app.route('/on_login', methods=['post'])
def on_login():
    user = User.query.filter_by(username=request.form['username']).first()
    if user == None:
        return redirect('/')
    elif bcrypt.check_password_hash(user.password, request.form['password']):
        session['userid'] = user.id
        return redirect('/dashboard')

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
        return render_template('dashboard.html', items=items)
    else:
        return render_template('dashboard.html')
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

if __name__ == "__main__":
    app.run(debug=True)