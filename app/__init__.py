# app/__init__.py
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS

from app.models import db
from app.routes.auth import auth_bp
from app.routes.referrals import referrals_bp
from app.config import Config

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

mail = Mail()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(referrals_bp, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        db.create_all()

    #rate limiting to protect against brute force attacks
    limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
    )

    # Apply specific limits to auth routes
    limiter.limit("5 per minute")(auth_bp)
    
    return app