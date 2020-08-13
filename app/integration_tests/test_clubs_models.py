from app.integration_tests import utils


def test_create_club(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    book_title = "a big old book"
    club_id = api_util.create_club(book_title=book_title).json()["id"]
    response = client.get(f"/club/{club_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"]
    assert data["book_title"] == book_title
    assert data["admin_user_id"] == 1
    assert data["users"][0]["id"] == 1
    assert len(data["users"]) == 1


def test_read_club(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    assert client.get(f"/club/1/").json()["id"] == 1
    assert client.get(f"/club/2/").json()["detail"] == "Club not found"


def test_read_clubs(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    assert len(client.get(f"/clubs/").json()["clubs"]) == 1

    api_util.create_user2_and_authenticate()  # switch to user 2

    assert not len(client.get(f"/clubs/").json()["clubs"])


def test_update_club_and_is_active_functionality(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    assert (
        client.put(
            "/club/2/", json={"is_active": False, "book_title": "Newish"}
        ).json()["detail"]
        == "Club not found"
    )

    client.put("/club/1/", json={"is_active": False, "book_title": "Newish"}).json()
    assert client.get("/club/1/").json()["is_active"] == False
    assert client.get("/club/1/").json()["book_title"] == "Newish"

    api_util.create_user2_and_authenticate()  # switch to user 2
    client.put(f"/club/1/join/")  # join the club
    assert (
        client.put(
            "/club/1/", json={"is_active": False, "book_title": "Newish"}
        ).json()["detail"]
        == "Club not updated, user is not admin"
    )

    api_util.authenticate()
    client.put("/club/1/", json={"is_active": False, "book_title": "Newish"})
    assert not len(client.get("/clubs/").json()["clubs"])


def test_join_club(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    api_util.create_user2_and_authenticate()  # switch to user 2
    client.put(f"/club/1/join/")  # join the club

    assert len(client.get("/club/1/").json()["users"]) == 2


def test_delete_club(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    client.delete("/club/1/")
    assert client.get("/club/1/").json()["detail"] == "Club not found"
    assert not len(client.get("/clubs/").json()["clubs"])

    api_util.create_club()
    api_util.create_user2_and_authenticate()  # switch to user 2
    client.put(f"/club/1/join/")  # join the club

    assert (
        client.delete("/club/1/").json()["detail"]
        == "Club not deleted, user is not admin"
    )
