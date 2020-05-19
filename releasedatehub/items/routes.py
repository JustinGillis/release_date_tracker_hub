from flask import Blueprint, render_template, redirect, request, abort, url_for, flash
from flask_login import current_user, login_required
from releasedatehub import db
from releasedatehub.models import Item
from releasedatehub.items.forms import ItemForm
from releasedatehub import newsapi


items = Blueprint('items', __name__)

@items.route('/item/new', methods=['GET', 'POST'])
@login_required
def new_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data, date=form.date.data, author=current_user)
        db.session.add(item)
        db.session.commit()
        flash('Your item has been added', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('new_item.html', title='New Item',
                             form=form, legend='New Item')

@items.route('/item/<int:id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('items.item', id=item.id))
    elif request.method == 'GET':
        print('in elif statement for GET')
        form.name.data = item.name
        form.date.data = item.date
    return render_template('new_item.html', item=item, form=form,
                             title='Update: '+item.name, legend='Update: '+item.name)

@items.route('/item/<int:id>/delete', methods=['POST'])
@login_required
def delete_item(id):
    item = Item.query.get_or_404(id)
    if item.author != current_user:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Your tracked item has been deleted', 'success')
    return redirect(url_for('main.dashboard'))

@items.route('/item/news/<name>')
@login_required
def item_news(name):
    news = newsapi.get_everything(q=f'{name} release', language='en')
    articles = news['articles']
    return render_template('item_news.html', articles=articles, title=name)

@items.route('/item/<int:id>')
@login_required
def item(id):
    item = Item.query.get_or_404(id)
    return render_template('item.html', item=item, title=item.name)