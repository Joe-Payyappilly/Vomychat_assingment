# app/services/email_service.py
from flask import current_app, render_template
from flask_mail import Message


def send_email(to, subject, template, **kwargs):
    """Send email"""
    from app import mail
    msg = Message(subject, recipients=[to])
    msg.html = render_template(template, **kwargs)
    mail.send(msg)

def send_password_reset_email(email, token):
    """Send password reset email"""
    reset_url = f"{current_app.config['FRONTEND_URL']}/reset-password?token={token}"
    send_email(
        to=email,
        subject="Password Reset",
        template="emails/password_reset.html",
        reset_url=reset_url,
        token=token
    )

def send_welcome_email(email, username):
    """Send welcome email to new user"""
    send_email(
        to=email,
        subject="Welcome to LinkShare!",
        template="emails/welcome.html",
        username=username
    )

def send_referral_success_email(referrer_email, referred_username):
    """Send email to referrer when someone signs up using their code"""
    send_email(
        to=referrer_email,
        subject="Someone joined using your referral!",
        template="emails/referral_success.html",
        referred_username=referred_username
    )