import pytest
from fastapi.testclient import TestClient

def test_end_to_end_signup_and_unregister(client: TestClient, reset_activities):
    """Test complete flow: signup then unregister"""
    email = "e2e_student@mergington.edu"
    activity = "Chess%20Club"

    # Initial state - check not signed up
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities["Chess Club"]["participants"]

    # Sign up
    response = client.post(f"/activities/{activity}/signup", json={"email": email})
    assert response.status_code == 200

    # Verify signed up
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Chess Club"]["participants"]

    # Unregister
    response = client.request("DELETE", f"/activities/{activity}/unregister", json={"email": email})
    assert response.status_code == 200

    # Verify unregistered
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities["Chess Club"]["participants"]

def test_end_to_end_capacity_management(client: TestClient, reset_activities):
    """Test capacity management: fill activity, try to add more, remove one, add again"""
    activity = "Programming%20Class"

    # Fill to capacity (max 20, currently 2)
    emails = []
    for i in range(18):
        email = f"capacity_test_{i}@mergington.edu"
        emails.append(email)
        response = client.post(f"/activities/{activity}/signup", json={"email": email})
        assert response.status_code == 200

    # Verify at capacity
    response = client.get("/activities")
    activities = response.json()
    assert len(activities["Programming Class"]["participants"]) == 20

    # Try to add one more - should fail
    response = client.post(f"/activities/{activity}/signup", json={"email": "over_capacity@mergington.edu"})
    assert response.status_code == 400

    # Remove one participant
    response = client.request("DELETE", f"/activities/{activity}/unregister", json={"email": emails[0]})
    assert response.status_code == 200

    # Now should be able to add one more
    response = client.post(f"/activities/{activity}/signup", json={"email": "now_can_add@mergington.edu"})
    assert response.status_code == 200

def test_end_to_end_multiple_activities(client: TestClient, reset_activities):
    """Test student signing up for multiple activities"""
    email = "multi_activity@mergington.edu"

    # Sign up for Chess Club
    response = client.post("/activities/Chess%20Club/signup", json={"email": email})
    assert response.status_code == 200

    # Sign up for Programming Class
    response = client.post("/activities/Programming%20Class/signup", json={"email": email})
    assert response.status_code == 200

    # Verify in both
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]

    # Unregister from one
    response = client.request("DELETE", "/activities/Chess%20Club/unregister", json={"email": email})
    assert response.status_code == 200

    # Verify removed from one but still in other
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]