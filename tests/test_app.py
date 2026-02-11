import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


@pytest.fixture(autouse=True)
def restore_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_success():
    email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_returns_400():
    email = "dup@mergington.edu"
    first = client.post("/activities/Chess Club/signup", params={"email": email})
    assert first.status_code == 200
    second = client.post("/activities/Chess Club/signup", params={"email": email})
    assert second.status_code == 400


def test_unregister_success():
    email = "toremove@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})
    response = client.delete("/activities/Chess Club/unregister", params={"email": email})
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]


def test_signup_missing_activity_404():
    response = client.post("/activities/Nope/signup", params={"email": "a@mergington.edu"})
    assert response.status_code == 404
