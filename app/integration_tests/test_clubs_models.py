from app.integration_tests import utils


def test_create_club(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    name = "We are a fun club"
    club_id = api_util.create_club(name=name).json()["id"]
    response = client.get(f"/club/{club_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"]
    assert data["name"] == name
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
        client.put("/club/2/", json={"is_active": False, "name": "Newish"}).json()[
            "detail"
        ]
        == "Club not found"
    )

    client.put("/club/1/", json={"is_active": False, "name": "Newish"}).json()
    assert client.get("/club/1/").json()["is_active"] == False
    assert client.get("/club/1/").json()["name"] == "Newish"

    api_util.create_user2_and_authenticate()  # switch to user 2
    client.put(f"/club/1/join/")  # join the club
    assert (
        client.put("/club/1/", json={"is_active": False, "name": "Newish"}).json()[
            "detail"
        ]
        == "Unauthorized, user is not club admin"
    )

    api_util.authenticate()
    client.put("/club/1/", json={"is_active": False, "name": "Newish"})
    assert not len(client.get("/clubs/").json()["clubs"])


def test_join_club(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    api_util.create_user2_and_authenticate()  # switch to user 2
    client.put(f"/club/1/join/")  # join the club

    assert len(client.get("/club/1/").json()["users"]) == 2


def test_add_book_to_club(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    club_id = api_util.create_club().json()["id"]
    book_id = api_util.create_book().json()["id"]

    client.put(f"/club/{club_id}/add_book/{book_id}/")

    assert len(client.get("/club/1/").json()["books"]) == 1


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
        == "Unauthorized, user is not club admin"
    )
