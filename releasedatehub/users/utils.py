import secrets
from flask import url_for
from flask_mail import Message
from releasedatehub import mail, db
from releasedatehub.models import Item
import datetime

SECRET_KEY = 'c006e7558c35ca45378686fd800fafa0aa'

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                    sender='release.date.hub@gmail.com',
                    recipients=[user.email])
    msg.body = f'''Click the link below to reset your password:
{url_for('users.reset_token', token=token, _external=True)}
    
If you did not make this request then ignore this email and no changes will be made.
'''
    mail.send(msg)

def send_notification_email():
    items = Item.query.all()
    Current_Date = datetime.date.today()
    for item in items:
        if item.date:
            item_date = item.date.date()
            if item_date >= Current_Date:
                if item.notification_emails_sent <= 7:
                    msg = Message(f'{item.name} has been released!',
                                    sender='release.date.hub@gmail.com',
                                    recipients=[item.author.email])
                    msg.body = f'''Hello {item.author.username},
{item.name} has finally been released. Wohoo!

If you do not want further reminders then please remove your tracker.

Thank you for using Release Date Tracker
'''
                    mail.send(msg)
                    item.notification_emails_sent = item.notification_emails_sent+1
                    db.session.commit()
