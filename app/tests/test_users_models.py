from app.tests import utils


def test_create_get_and_update_user(client):
    team_id = "T0140PRK962"
    api_util = utils.MockApiRequests(client)
    response = api_util.create_user(team_id=team_id)
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == f"No team exists for specified team_id: {team_id}"

    response = api_util.create_team(team_id=team_id)
    assert response.status_code == 200, response.text

    response = api_util.create_user(team_id=team_id)
    assert response.status_code == 200, response.text
    data = response.json()
    slack_id_team_id = data["slack_id_team_id"]
    assert slack_id_team_id == "U014YSCLQ2X_T0140PRK962"
    assert data["name"] == "Patrick M Kelly"

    response = client.get(f"/user/{slack_id_team_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Patrick M Kelly"
    assert data["slack_id_team_id"] == "U014YSCLQ2X_T0140PRK962"

    my_new_name = "Not Patrick Anymore!"
    response = api_util.update_user(slack_id_team_id, name=my_new_name)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == my_new_name

    response = client.delete(f"/user/{slack_id_team_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["slack_id_team_id"] == slack_id_team_id
    response = client.get(f"/user/{slack_id_team_id}/")
    data = response.json()
    assert response.status_code == 400, response.text
    assert data["detail"] == "User not found"
