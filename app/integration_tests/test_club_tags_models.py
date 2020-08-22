from app.integration_tests import utils


def test_create_club_tag(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_book()
    api_util.create_club()

    response = api_util.create_club_tag(name="a new tag name")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "a new tag name"


def test_read_club_tag(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_book()
    api_util.create_club()
    api_util.create_club_tag(name="test getter")

    assert client.get(f"/api/club_tag/1/").json()["name"] == "test getter"
    assert client.get(f"/api/club_tag/2/").json()["detail"] == "ClubTag not found"


def test_read_club_tags(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_book()
    api_util.create_club()

    api_util.create_club_tag(name="test getter")
    assert (
        client.get(f"/api/club_tags/?club_id=1").json()["club_tags"][0]["name"]
        == "test getter"
    )

    api_util.create_user2_and_authenticate()  # create/login as another user
    assert (
        client.get(f"/api/club_tags/?club_id=1").json()["detail"] == "ClubTag not found"
    )
    client.put(f"/api/club/1/join/")  # join the club

    api_util.create_club_tag(name="test getter2")
    assert (
        client.get(f"/api/club_tags/?club_id=1").json()["club_tags"][1]["name"]
        == "test getter2"
    )


def test_update_club_tag_and_archived_functionality(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_book()
    api_util.create_club()

    api_util.create_club_tag(name="test create")
    api_util.update_club_tag(club_tag_id=1, name="test update", archived=True)
    assert client.get(f"/api/club_tag/1/").json()["name"] == "test update"
    assert client.get(f"/api/club_tag/1/").json()["archived"] == True


def test_delete_club_tag(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_book()
    api_util.create_club()

    api_util.create_club_tag(name="test create")
    client.delete("/api/club_tag/1/")
    assert client.get("/api/club_tag/1/").json()["detail"] == "ClubTag not found"

    api_util.create_club_tag(name="test create")
    api_util.create_user2_and_authenticate()  # create/login as another user
    ### Fails because user is not admin
    assert client.delete("/api/club_tag/1/").json()["detail"] == "ClubTag not found"
