from app.tests import utils


def test_create_get_update_and_delete_club(client):
    api_util = utils.MockApiRequests(client)
    response = api_util.create_user()
    data = response.json()
    user_id = data["id"]
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
    assert data["admin_user_id"] == user_id
    assert not data["users"]

    response = client.get(f"/club/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data["clubs"]) == 1

    new_book_title = "Decolonizing Wealth"
    response = client.put(f"/club/{club_id}/", json={"book_title": new_book_title},)
    assert response.status_code == 200, response.text
    response = client.get(f"/club/{club_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["book_title"] == new_book_title

    response = api_util.create_user(full_name="User 2",)
    data = response.json()
    user_2 = data["id"]
    response = client.put(f"/club/{club_id}/add_user/{user_2}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["users"][0]["id"] == user_2

    response = client.get(f"/club/?user_id={user_2}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data["clubs"]) == 1

    response = client.delete(f"/club/{club_id}/")
    assert response.status_code == 200, response.text
    response = client.get(f"/club/{club_id}/")
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Club not found"

    response = client.get(f"/club/?user_id={user_2}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data["clubs"]) == 0
