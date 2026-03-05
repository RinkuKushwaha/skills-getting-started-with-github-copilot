import pytest
from fastapi.testclient import TestClient

def test_get_activities_success(client: TestClient, reset_activities):
    """Test successful retrieval of all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()

    # Check that we get a dict with activity names as keys
    assert isinstance(data, dict)
    assert len(data) > 0

    # Check structure of first activity
    first_activity = next(iter(data.values()))
    assert "description" in first_activity
    assert "schedule" in first_activity
    assert "max_participants" in first_activity
    assert "participants" in first_activity
    assert isinstance(first_activity["participants"], list)

def test_get_activities_contains_expected_activities(client: TestClient, reset_activities):
    """Test that expected activities are present"""
    response = client.get("/activities")
    data = response.json()

    assert "Chess Club" in data
    assert "Programming Class" in data

    # Check specific activity details
    chess_club = data["Chess Club"]
    assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
    assert chess_club["max_participants"] == 12
    assert len(chess_club["participants"]) == 2