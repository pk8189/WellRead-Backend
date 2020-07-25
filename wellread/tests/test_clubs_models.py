from wellread.tests import utils


def test_create_get_update_and_delete_club(client):
    api_util = utils.MockApiRequests(client)
    team_id = "T0140PRK962"
    response = api_util.create_team(team_id=team_id)
    user_id = "U014YSCLQ2X_T0140PRK962"
    response = api_util.create_user(team_id=team_id, slack_id_team_id=user_id)
    book_title = "a big old book"
    response = api_util.create_club(book_title=book_title, admin_user_id=user_id)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"]
    assert data["book_title"] == book_title

    club_id = data["id"]
    response = client.get(f"/club/{club_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["channel_id"] == "19WEWFJEW1425W"
    assert data["admin_user_id"] == user_id
    assert not data["slack_users"]

    new_book_title = "Decolonizing Wealth"
    response = client.put(f"/club/{club_id}/", json={"book_title": new_book_title})
    assert response.status_code == 200, response.text
    response = client.get(f"/club/{club_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["book_title"] == new_book_title

    user_2 = "ALKAFKLJSDFKLJ"
    api_util.create_user(
        slack_id_team_id=user_2, name="User 2", team_id=team_id,
    )
    response = client.put(f"/club/{club_id}/add_user/{user_2}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["slack_users"][0]["slack_id_team_id"] == user_2

    response = client.delete(f"/club/{club_id}/")
    assert response.status_code == 200, response.text
    response = client.get(f"/club/{club_id}/")
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Club not found"
