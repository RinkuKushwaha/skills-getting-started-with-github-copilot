import pytest
from fastapi.testclient import TestClient

def test_unregister_success(client: TestClient, reset_activities):
    """Test successful unregistration from an activity"""
    response = client.request("DELETE", "/activities/Chess%20Club/unregister", json={"email": "michael@mergington.edu"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "michael@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]

def test_unregister_activity_not_found(client: TestClient, reset_activities):
    """Test unregister from non-existent activity"""
    response = client.request("DELETE", "/activities/NonExistent/unregister", json={"email": "student@mergington.edu"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_unregister_not_signed_up(client: TestClient, reset_activities):
    """Test unregister when student is not signed up"""
    response = client.request("DELETE", "/activities/Chess%20Club/unregister", json={"email": "notsignedup@mergington.edu"})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student is not signed up for this activity"

def test_unregister_invalid_email_format(client: TestClient, reset_activities):
    """Test unregister with invalid email format"""
    response = client.request("DELETE", "/activities/Chess%20Club/unregister", json={"email": "invalid-email"})
    assert response.status_code == 422  # Pydantic validation error

def test_unregister_missing_email(client: TestClient, reset_activities):
    """Test unregister with missing email field"""
    response = client.request("DELETE", "/activities/Chess%20Club/unregister", json={})
    assert response.status_code == 422  # Pydantic validation error