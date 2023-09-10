from flask import render_template

from app import mail, Message
from app.utils.helper import get_env


def send_email(to, subject, template, **kwargs):
    sender_email = get_env('MAIL_USERNAME')
    msg = Message(subject, sender=sender_email, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
