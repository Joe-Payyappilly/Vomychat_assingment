# app/models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
import uuid
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column('password', db.String(128), nullable=False)
    referral_code = db.Column(db.String(20), unique=True, nullable=False)
    referred_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    referred_by = db.relationship('User', remote_side=[id], backref='referrals')
    
    def __init__(self, username, email, password, referred_by=None):
        self.username = username
        self.email = email
        self.password = password
        self.referral_code = self.generate_referral_code()
        self.referred_by = referred_by
    
    @hybrid_property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, plaintext_password):
        self._password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, plaintext_password):
        return bcrypt.checkpw(plaintext_password.encode('utf-8'), self.password.encode('utf-8'))
    
    def generate_referral_code(self):
        return str(uuid.uuid4())[:8]

class PasswordReset(db.Model):
    __tablename__ = 'password_resets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='password_resets')

class Referral(db.Model):
    __tablename__ = 'referrals'
    
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    referred_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_referred = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='successful')  # pending, successful, etc.
    
    # Relationships
    referrer = db.relationship('User', foreign_keys=[referrer_id], backref='referrals_made')
    referred_user = db.relationship('User', foreign_keys=[referred_user_id], backref='referral_info')

# Optional Rewards table
class Reward(db.Model):
    __tablename__ = 'rewards'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    referral_id = db.Column(db.Integer, db.ForeignKey('referrals.id'), nullable=False)
    reward_type = db.Column(db.String(50), nullable=False)  # e.g., "credit", "premium_feature"
    amount = db.Column(db.Float, nullable=True)  # if applicable
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='rewards')
    referral = db.relationship('Referral', backref='rewards')