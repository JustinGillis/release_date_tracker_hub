import secrets
from flask import url_for
from flask_mail import Message
from releasedatehub import app, mail

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                    sender='mr.snoogi@gmail.com',
                    recipients=[user.email])
    msg.body = f'''Click the link below to reset your password:
{url_for('users.reset_token', token=token, _external=True)}
    
If you did not make this request then ignore this email and no changes will be made.
'''
    mail.send(msg)