"""
Tests for FastAPI activities endpoints using AAA (Arrange-Act-Assert) pattern.
"""
import pytest


def test_get_activities_success(client):
    # Arrange: (Nothing to set up, uses default data)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_not_found(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_unregister_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_not_signed_up(client):
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_activity_not_found(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
