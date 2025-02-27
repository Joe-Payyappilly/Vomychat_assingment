def test_register_with_valid_referral(client):
    """Test registering a user with a valid referral code."""
    referrer_response = client.post("/api/register", json={
        "username": "referrer",
        "email": "referrer@example.com",
        "password": "Password123"
    })
    referrer_code = referrer_response.get_json()["user"]["referral_code"]

    response = client.post("/api/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "Password123",
        "referral_code": referrer_code
    })
    assert response.status_code == 201
    assert response.get_json()["success"] is True

def test_register_with_invalid_referral(client):
    """Test registering with an invalid referral code."""
    response = client.post("/api/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "Password123",
        "referral_code": "INVALIDCODE"
    })
    assert response.status_code == 400
    assert response.get_json()["message"] == "Invalid referral code"

def test_user_cannot_refer_themselves(client):
    """Test that users cannot refer themselves."""
    user_response = client.post("/api/register", json={
        "username": "selfreferrer",
        "email": "selfreferrer@example.com",
        "password": "Password123"
    })
    referral_code = user_response.get_json()["user"]["referral_code"]

    response = client.post("/api/register", json={
        "username": "selfreferrer",
        "email": "selfreferrer@example.com",
        "password": "Password123",
        "referral_code": referral_code
    })

    print("Response JSON:", response.get_json())  # Debugging output
    assert response.status_code == 400
    assert "message" in response.get_json(), f"Actual response: {response.get_json()}"
    assert response.get_json()["message"] == "You cannot refer yourself"


def test_referral_count_updates(client):
    """Test that referrals are tracked correctly."""
    referrer_response = client.post("/api/register", json={
        "username": "referrer",
        "email": "referrer@example.com",
        "password": "Password123"
    })
    referrer_code = referrer_response.get_json()["user"]["referral_code"]

    client.post("/api/register", json={
        "username": "referred1",
        "email": "referred1@example.com",
        "password": "Password123",
        "referral_code": referrer_code
    })

    client.post("/api/register", json={
        "username": "referred2",
        "email": "referred2@example.com",
        "password": "Password123",
        "referral_code": referrer_code
    })

    # Fetch referral stats
    referrer_login = client.post("/api/login", json={
        "username_or_email": "referrer@example.com",
        "password": "Password123"
    })
    token = referrer_login.get_json()["access_token"]

    response = client.get("/api/referral-stats", headers={"Authorization": f"Bearer {token}"})
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["stats"]["total_referrals"] == 2
