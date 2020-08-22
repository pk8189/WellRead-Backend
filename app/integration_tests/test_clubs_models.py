from app.integration_tests import utils


def test_create_club(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    name = "We are a fun club"
    club_id = api_util.create_club(name=name).json()["id"]
    response = client.get(f"/api/club/{club_id}/")
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

    assert client.get(f"/api/club/1/").json()["id"] == 1
    assert client.get(f"/api/club/2/").json()["detail"] == "Club not found"


def test_read_clubs(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    assert len(client.get(f"/api/clubs/").json()["clubs"]) == 1

    api_util.create_user2_and_authenticate()  # switch to user 2

    assert not len(client.get(f"/api/clubs/").json()["clubs"])


def test_update_club_and_is_active_functionality(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    assert (
        client.put("/api/club/2/", json={"is_active": False, "name": "Newish"}).json()[
            "detail"
        ]
        == "Club not found"
    )

    client.put("/api/club/1/", json={"is_active": False, "name": "Newish"}).json()
    assert client.get("/api/club/1/").json()["is_active"] == False
    assert client.get("/api/club/1/").json()["name"] == "Newish"

    api_util.create_user2_and_authenticate()  # switch to user 2
    client.put(f"/api/club/1/join/")  # join the club

    api_util.authenticate()
    client.put("/api/club/1/", json={"is_active": False, "name": "Newish"})
    assert not len(client.get("/api/clubs/").json()["clubs"])


def test_join_club(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    api_util.create_user2_and_authenticate()  # switch to user 2
    client.put(f"/api/club/1/join/")  # join the club

    assert len(client.get("/api/club/1/").json()["users"]) == 2


def test_add_and_remove_book_to_club(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    club_id = api_util.create_club().json()["id"]
    book_id = api_util.create_book().json()["id"]

    client.put(f"/api/club/{club_id}/book/{book_id}/add/")
    assert len(client.get("/api/club/1/").json()["books"]) == 1

    client.put(f"/api/club/{club_id}/book/{book_id}/remove/")
    assert len(client.get("/api/club/1/").json()["books"]) == 0


def test_delete_club(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    client.delete("/api/club/1/")
    assert client.get("/api/club/1/").json()["detail"] == "Club not found"
    assert not len(client.get("/api/clubs/").json()["clubs"])

    api_util.create_club()
    api_util.create_user2_and_authenticate()  # switch to user 2
    client.put(f"/api/club/1/join/")  # join the club

    assert (
        client.delete("/api/club/1/").json()["detail"] == "Non-admin cannot delete club"
    )
