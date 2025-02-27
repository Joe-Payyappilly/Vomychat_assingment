import json
from app.models import User

def test_register_success(client):
    """Test successful user registration."""
    response = client.post("/api/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "SecurePass123",
        "referral_code": None
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert "access_token" in data

def test_register_existing_email(client):
    """Test registration with an already registered email."""
    client.post("/api/register", json={
        "username": "user1",
        "email": "existing@example.com",
        "password": "Pass123"
    })
    response = client.post("/api/register", json={
        "username": "user2",
        "email": "existing@example.com",
        "password": "Pass123"
    })
    assert response.status_code == 400
    assert "errors" in response.get_json()

def test_login_success(client):
    """Test successful login."""
    client.post("/api/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "Password123"
    })
    response = client.post("/api/login", json={
        "username_or_email": "login@example.com",
        "password": "Password123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data

def test_login_invalid_credentials(client):
    """Test login with incorrect password."""
    client.post("/api/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "Password123"
    })
    response = client.post("/api/login", json={
        "username_or_email": "login@example.com",
        "password": "WrongPass"
    })
    assert response.status_code == 401
    assert response.get_json()["message"] == "Invalid credentials"
