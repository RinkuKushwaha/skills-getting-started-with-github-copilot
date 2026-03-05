import pytest
from fastapi.testclient import TestClient

def test_signup_success(client: TestClient, reset_activities):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Chess%20Club/signup",
        json={"email": "newstudent@mergington.edu"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]

def test_signup_activity_not_found(client: TestClient, reset_activities):
    """Test signup for non-existent activity"""
    response = client.post(
        "/activities/NonExistent/signup",
        json={"email": "student@mergington.edu"}
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_signup_already_signed_up(client: TestClient, reset_activities):
    """Test signup when student is already signed up"""
    response = client.post(
        "/activities/Chess%20Club/signup",
        json={"email": "michael@mergington.edu"}  # Already in Chess Club
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student is already signed up for this activity"

def test_signup_at_capacity(client: TestClient, reset_activities):
    """Test signup when activity is at maximum capacity"""
    # First fill up Programming Class (max 20, currently 2 participants)
    for i in range(18):
        response = client.post(
            "/activities/Programming%20Class/signup",
            json={"email": f"student{i}@mergington.edu"}
        )
        assert response.status_code == 200

    # Now try to add one more - should fail
    response = client.post(
        "/activities/Programming%20Class/signup",
        json={"email": "laststudent@mergington.edu"}
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Activity is at maximum capacity"

def test_signup_invalid_email_format(client: TestClient, reset_activities):
    """Test signup with invalid email format"""
    response = client.post(
        "/activities/Chess%20Club/signup",
        json={"email": "invalid-email"}
    )
    assert response.status_code == 422  # Pydantic validation error

def test_signup_missing_email(client: TestClient, reset_activities):
    """Test signup with missing email field"""
    response = client.post(
        "/activities/Chess%20Club/signup",
        json={}
    )
    assert response.status_code == 422  # Pydantic validation error