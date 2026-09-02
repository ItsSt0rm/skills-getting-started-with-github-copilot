from fastapi.testclient import TestClient

import src.app as app_module

client = TestClient(app_module.app)


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_error():
    activity_name = "Chess Club"
    email = "not-a-member@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 404
    assert "not signed up" in response.json()["detail"].lower()
