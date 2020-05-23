import secrets
from flask import url_for
from flask_mail import Message
from releasedatehub import mail, db

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

def send_notification_email(user, item):
    msg = Message(f'{item.title} has been released!',
                    sender='release.date.hub@gmail.com',
                    recipients=[user.email])
    msg.body = f'''Hello {user.username},
{item.title} has finally been release! Wohoo!
Thank you for using Release Date Tracker :)
'''
    mail.send(msg)
    item.notification_emails_sent += 1