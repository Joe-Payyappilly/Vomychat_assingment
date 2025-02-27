# app/services/auth_service.py
from datetime import datetime, timedelta
import uuid
from flask import current_app
from flask_jwt_extended import create_access_token

from app.models import db, User, PasswordReset
from app.services.email_service import send_password_reset_email

def register_user(username, email, password, referral_code=None):
    """Register a new user"""
    referred_by = None
    if referral_code:
        referred_by = User.query.filter_by(referral_code=referral_code).first()
        if not referred_by:
            raise ValueError("Invalid referral code")  # <-- Raise an error for invalid referral

    # Prevent self-referral
    if referred_by and referred_by.email == email:
        raise ValueError("You cannot refer yourself")  # <-- Prevent self-referral

    # Create new user
    user = User(username=username, email=email, password=password, referred_by=referred_by)

    # Add to database
    db.session.add(user)
    db.session.commit()

    # Create referral record if user was referred
    if referred_by:
        from app.services.referral_service import create_referral
        create_referral(referred_by.id, user.id)

    return user




def authenticate_user(username_or_email, password):
    """Authenticate user credentials"""
    # Check if input is email or username
    if '@' in username_or_email:
        user = User.query.filter_by(email=username_or_email).first()
    else:
        user = User.query.filter_by(username=username_or_email).first()
    
    if user and user.verify_password(password):
        return user
    
    return None

def create_user_token(user_id):
    """Create JWT token for user"""
    access_token = create_access_token(identity=user_id)
    return access_token

def initiate_password_reset(email):
    """Generate password reset token and send email"""
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    
    # Generate token
    token = str(uuid.uuid4())
    
    # Save token to database
    reset = PasswordReset(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )
    
    db.session.add(reset)
    db.session.commit()
    
    # Send email
    send_password_reset_email(user.email, token)
    
    return True

def reset_password(token, new_password):
    """Reset user password using token"""
    reset = PasswordReset.query.filter_by(token=token).first()
    
    if not reset or reset.expires_at < datetime.utcnow():
        return False
    
    user = User.query.get(reset.user_id)
    user.password = new_password
    
    # Delete all reset tokens for this user
    PasswordReset.query.filter_by(user_id=user.id).delete()
    
    db.session.commit()
    
    return True