from flask import render_template, request, redirect, session, url_for, flash

from releasedatehub import app, db
from releasedatehub.forms import RegistrationForm, LoginForm
from releasedatehub.models import User, Item

import re
from newsapi import NewsApiClient
from flask_bcrypt import Bcrypt 
from dateutil.parser import parse

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)
newsapi = NewsApiClient(api_key='571610756dbb460298a1abbe29199de9')


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
        item = Item(name=request.form['name'], date = python_date, user_id = session['userid'])
        db.session.add(item)
        db.session.commit()
        print('finished date found statement')

    else:
        print('no date found')
        item = Item(name=request.form['name'], user_id=session['userid'])
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
    items = Item.query.filter_by(user_id=session['userid'])
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