import pytest
from src import app as app_module

# Test root redirect

def test_root_redirect(client):
    # Arrange: nothing to set up
    # Act
    resp = client.get("/", follow_redirects=False)
    # Assert
    assert resp.status_code in (307, 308)
    assert resp.headers["location"].endswith("/static/index.html")

# Test GET /activities

def test_get_activities(client):
    # Arrange: nothing to set up
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

# Test POST /activities/{activity}/signup (success)

def test_signup_success(client):
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Science Club"
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]

# Test POST /activities/{activity}/signup (duplicate)

def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = app_module.activities[activity]["participants"][0]
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student already signed up"

# Test POST /activities/{activity}/signup (not found)

def test_signup_not_found(client):
    # Arrange
    activity = "NoSuchActivity"
    email = "a@b.com"
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 404

# Test DELETE /activities/{activity}/participants (success)

def test_unregister_success(client):
    # Arrange
    activity = "Drama Club"
    email = app_module.activities[activity]["participants"][0]
    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert email not in app_module.activities[activity]["participants"]

# Test DELETE /activities/{activity}/participants (activity not found)

def test_unregister_activity_not_found(client):
    # Arrange
    activity = "NoAct"
    email = "foo@bar.com"
    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert
    assert resp.status_code == 404

# Test DELETE /activities/{activity}/participants (participant not found)

def test_unregister_participant_not_found(client):
    # Arrange
    activity = "Chess Club"
    email = "noone@mergington.edu"
    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert
    assert resp.status_code == 404
