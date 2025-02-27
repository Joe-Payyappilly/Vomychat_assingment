# app/utils/validators.py
import re
from app.models import User

def validate_email(email):
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_password_strength(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    
    return True, "Password is strong enough"

def is_username_taken(username):
    """Check if username already exists"""
    return User.query.filter_by(username=username).first() is not None

def is_email_taken(email):
    """Check if email already exists"""
    return User.query.filter_by(email=email).first() is not None

def validate_registration_data(username, email, password):
    """Validate registration data"""
    errors = {}
    
    if not username or len(username) < 3:
        errors['username'] = "Username must be at least 3 characters long"
    
    if is_username_taken(username):
        errors['username'] = "Username is already taken"
    
    if not validate_email(email):
        errors['email'] = "Invalid email format"
    
    if is_email_taken(email):
        errors['email'] = "Email is already registered"
    
    is_valid, password_error = validate_password_strength(password)
    if not is_valid:
        errors['password'] = password_error
    
    return len(errors) == 0, errors