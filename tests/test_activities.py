from urllib.parse import quote


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_participant(client):
    activity = "Chess Club"
    email = "newstudent@example.com"
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # verify state changed
    resp2 = client.get("/activities")
    assert email in resp2.json()[activity]["participants"]


def test_signup_duplicate(client):
    activity = "Chess Club"
    existing = "michael@mergington.edu"
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": existing})
    assert resp.status_code == 400


def test_delete_participant(client):
    activity = "Chess Club"
    email = "michael@mergington.edu"
    resp = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})
    assert resp.status_code == 200
    assert resp.json().get("removed", 0) >= 1

    # verify state changed
    resp2 = client.get("/activities")
    assert email not in resp2.json()[activity]["participants"]


def test_delete_nonexistent(client):
    activity = "Chess Club"
    email = "noone@nowhere.com"
    resp = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})
    assert resp.status_code == 404


def test_signup_nonexistent_activity(client):
    activity = "Nonexistent"
    email = "someone@example.com"
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert resp.status_code == 404
