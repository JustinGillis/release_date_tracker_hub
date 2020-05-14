from flask import render_template, request, redirect, session, url_for, flash, abort

from releasedatehub import app, db
from releasedatehub.forms import RegistrationForm, LoginForm, UpdateAccountForm, ItemForm, RequestResetForm, ResetPasswordForm
from releasedatehub.models import User, Item
from flask_login import login_user, logout_user, current_user, login_required
 
import re
from newsapi import NewsApiClient
from flask_bcrypt import Bcrypt 
from dateutil.parser import parse

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)
newsapi = NewsApiClient(api_key='571610756dbb460298a1abbe29199de9')


@app.route('/')
def home():
    # add homepage content
    return render_template('home.html')

@app.route('/about')
def about():
    # add content
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,
                         email=form.email.data, password=pw_hash)
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have logged in', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login unsucccessful', 'danger')
    return render_template('login.html', title='Log In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/item/new', methods=['GET', 'POST'])
@login_required
def new_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data, date=form.date.data, author=current_user)
        db.session.add(item)
        db.session.commit()
        flash('Your item has been added', 'success')
        return redirect(url_for('dashboard'))
    return render_template('new_item.html', title='New Item',
                             form=form, legend='New Item')

@app.route('/item/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    print('in update route')
    item = Item.query.get_or_404(id)
    if item.author != current_user:
        print('aborting...')
        abort(403)
    form = ItemForm()
    if form.validate_on_submit():
        print('form validated on submit')
        item.name = form.name.data
        item.date = form.date.data
        db.session.commit()
        print('form commited')
        flash('Your tracked item has been updated', 'success')
        print('redirecting')
        return redirect(url_for('item', id=item.id))
    elif request.method == 'GET':
        print('in elif statement for GET')
        form.name.data = item.name
        form.date.data = item.date
    return render_template('new_item.html', item=item, form=form,
                             title='Update: '+item.name, legend='Update: '+item.name)

@app.route('/item/<int:id>/delete', methods=['POST'])
@login_required
def delete_item(id):
    item = Item.query.get_or_404(id)
    if item.author != current_user:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Your tracked item has been deleted', 'success')
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    items = Item.query.filter_by(user_id=current_user.id)
    if items:
        return render_template('dashboard.html', items=items, title='Dashboard')
    else:
        return render_template('dashboard.html', title='Dashboard')
    # add news article notification logic

@app.route('/item/news/<name>')
@login_required
def item_news(name):
    news = newsapi.get_everything(q=f'{name} release', language='en')
    articles = news['articles']
    return render_template('item_news.html', articles=articles, title=name)

@app.route('/item/<int:id>')
@login_required
def item(id):
    item = Item.query.get_or_404(id)
    return render_template('item.html', item=item, title=item.name)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


def send_reset_email(user):
    pass


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    return render_template('reset_token.html', title='Reset Password', form=form)