from app.tests import utils


def test_create_and_get_team(client):
    api_util = utils.MockApiRequests(client)
    response = api_util.create_team()
    assert response.status_code == 200, response.text
    data = response.json()
    team_id = data["team_id"]
    assert team_id == "T0140PRK962"
    assert data["name"] == "WellRead"

    response = client.get(f"/team/{team_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "WellRead"
    assert data["team_id"] == team_id


def test_create_and_delete_team(client):
    api_util = utils.MockApiRequests(client)
    response = api_util.create_team(
        team_id="T0140PRK961", name="To Be Deleted!", domain="www.domain.com"
    )
    assert response.status_code == 200, response.text
    data = response.json()
    team_id = data["team_id"]
    response = client.delete(f"/team/{team_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["team_id"] == team_id
    response = client.get(f"/team/{team_id}/")
    data = response.json()
    assert response.status_code == 400, response.text
    assert data["detail"] == "Team not found"
