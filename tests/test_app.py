import urllib.parse

def test_root_redirects_to_index(client):
    # Arrange: client fixture
    # Act
    resp = client.get("/")

    # Assert
    assert resp.status_code == 307
    assert resp.headers.get("location") == "/static/index.html"


def test_get_activities_returns_expected_structure(client):
    # Arrange
    # Act
    resp = client.get("/activities")
    data = resp.json()

    # Assert
    assert resp.status_code == 200
    assert isinstance(data, dict)
    # check one known activity has expected keys
    sample = next(iter(data.values()))
    assert "description" in sample
    assert "schedule" in sample
    assert "max_participants" in sample
    assert "participants" in sample


def test_signup_success_adds_participant(client, appmod):
    # Arrange
    activity = "Art Studio"
    email = "tester@example.com"
    # ensure email not already present
    if email in appmod.activities[activity]["participants"]:
        appmod.activities[activity]["participants"].remove(email)

    # Act
    url_activity = urllib.parse.quote(activity, safe="")
    resp = client.post(f"/activities/{url_activity}/signup?email={urllib.parse.quote(email, safe='')}")

    # Assert
    assert resp.status_code == 200
    assert email in appmod.activities[activity]["participants"]


def test_signup_duplicate_is_400(client, appmod):
    # Arrange
    activity = "Basketball Team"
    email = "duplicate@example.com"
    # ensure email present
    if email not in appmod.activities[activity]["participants"]:
        appmod.activities[activity]["participants"].append(email)

    # Act
    url_activity = urllib.parse.quote(activity, safe="")
    resp = client.post(f"/activities/{url_activity}/signup?email={urllib.parse.quote(email, safe='')}")

    # Assert
    assert resp.status_code == 400


def test_signup_missing_activity_is_404(client):
    # Arrange
    activity = "Nonexistent Activity"
    email = "noone@example.com"

    # Act
    url_activity = urllib.parse.quote(activity, safe="")
    resp = client.post(f"/activities/{url_activity}/signup?email={urllib.parse.quote(email, safe='')}")

    # Assert
    assert resp.status_code == 404


def test_unregister_success_removes_participant(client, appmod):
    # Arrange
    activity = "Drama Club"
    email = "remove_me@example.com"
    if email not in appmod.activities[activity]["participants"]:
        appmod.activities[activity]["participants"].append(email)

    # Act
    url_activity = urllib.parse.quote(activity, safe="")
    resp = client.delete(f"/activities/{url_activity}/participants?email={urllib.parse.quote(email, safe='')}")

    # Assert
    assert resp.status_code == 200
    assert email not in appmod.activities[activity]["participants"]


def test_unregister_not_registered_is_404(client, appmod):
    # Arrange
    activity = "Math Club"
    email = "notregistered@example.com"
    if email in appmod.activities[activity]["participants"]:
        appmod.activities[activity]["participants"].remove(email)

    # Act
    url_activity = urllib.parse.quote(activity, safe="")
    resp = client.delete(f"/activities/{url_activity}/participants?email={urllib.parse.quote(email, safe='')}")

    # Assert
    assert resp.status_code == 404
