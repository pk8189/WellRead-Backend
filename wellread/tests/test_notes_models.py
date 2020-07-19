from wellread.tests import utils


def test_create_notes(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_team()
    no_user_res = api_util.create_note()
    assert no_user_res.status_code == 400
    api_util.create_user()
    no_club_res = api_util.create_note()
    assert no_club_res.status_code == 400
    api_util.create_club()
    response = api_util.create_note()
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"]
    assert data["content"] == "Oh my, such a lovely note!"
