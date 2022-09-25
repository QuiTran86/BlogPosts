from flask import render_template, current_app
from flask_mail import Message, Mail


def send_email_in_context(message):
    with current_app.app_context():
        mail = Mail(current_app)
        mail.send(message)


def send_email(subject, template, to, **kwargs):

    message = Message(subject, sender=current_app.config['FLASKY_ADMIN'], recipients=[to])
    message.body = render_template(template, **kwargs)
    send_email_in_context(message)
