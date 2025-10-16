import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Ensure not already signed up
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    # Try signing up again (should fail)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400


def test_unregister_from_activity():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Ensure signed up
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]
    # Try unregistering again (should fail)
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400


def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404


def test_unregister_invalid_activity():
    response = client.delete("/activities/Nonexistent/unregister?email=test@mergington.edu")
    assert response.status_code == 404


def test_unregister_not_registered():
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
