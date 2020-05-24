from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'release.date.hub@gmail.com',
	MAIL_PASSWORD = 'Gp2js8!30'
	)
mail = Mail(app)

def send_mail():
    print('in send mail function')
    msg = Message("Just a Test!",
        sender="release.date.hub@gmail.com",
        recipients=["mr.snoogi@gmail.com"])
    msg.body = "Did this work?"           
    mail.send(msg)
    print('exiting send mail function')

send_mail()