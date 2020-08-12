from app.integration_tests import utils


def test_create_get_update_and_delete_club(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()  # creates a user and authenticates the client

    book_title = "a big old book"
    response = api_util.create_club(book_title=book_title)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"]
    assert data["book_title"] == book_title
    assert data["admin_user_id"] == 1
    assert data["users"][0]["id"] == 1
    assert len(data["users"]) == 1

    club_id = data["id"]
    response = client.get(f"/club/{club_id}/")
    assert response.status_code == 200, response.text
    data = response.json()

    response = client.get(f"/club/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data["clubs"]) == 1

    new_book_title = "Decolonizing Wealth"
    response = client.put(
        f"/club/{club_id}/", json={"book_title": new_book_title, "is_active": False}
    )
    assert response.status_code == 200, response.text
    response = client.get(f"/club/{club_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["book_title"] == new_book_title
    assert data["is_active"] == False
    client.put(f"/club/{club_id}/", json={"is_active": True})

    api_util.create_user2_and_authenticate()  # switch to user 2

    response = client.put(f"/club/{club_id}/join/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["users"][1]["id"] == 2
    assert len(data["users"]) == 2

    response = client.get(f"/club/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data["clubs"]) == 1

    response = client.delete(f"/club/{club_id}/")
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Club not deleted, user is not admin"

    api_util.authenticate()  # switch back to user 1
    response = client.delete(f"/club/{club_id}/")
    assert response.status_code == 200, response.text

    response = client.get(f"/club/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data["clubs"]) == 0

    api_util.authenticate(
        email="anotheruser@gmail.com", password="password2"
    )  # switch back to user 1
    response = client.get(f"/club/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data["clubs"]) == 0
