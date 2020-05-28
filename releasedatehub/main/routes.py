from flask import render_template, request, Blueprint
from flask_login import current_user, login_required
from releasedatehub.models import Item

main = Blueprint('main', __name__)

@main.route('/')
def home():
    # add homepage content
    return render_template('home.html', main_formatting="col-md-8", side_content_format="col-md-4")

@main.route('/about')
def about():
    # add about content
    return render_template('about.html')

@main.route('/dashboard')
@login_required
def dashboard():
    items = Item.query.filter_by(user_id=current_user.id)
    if items:
        return render_template('dashboard.html', items=items, title='Dashboard')
    else:
        return render_template('dashboard.html', title='Dashboard')
    # add news article notification logic