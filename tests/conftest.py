import sys
import os

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
import pytest

@pytest.fixture
def app():
    """Create and configure a new app instance for testing"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret-key",
        "MAIL_SUPPRESS_SEND": True
    })
    
    with app.app_context():
        db.create_all()
    
    yield app  # Provide the app instance for tests
    
    # Cleanup
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()
