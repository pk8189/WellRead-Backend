from app.integration_tests import utils


def test_create_tag(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    response = api_util.create_tag()
    data = response.json()
    assert response.status_code == 400, response.text
    assert data["detail"] == "Club does not exist or not member"

    api_util.create_club()
    response = api_util.create_tag(name="a new tag name")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "a new tag name"


def test_read_tag(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    club_id = api_util.create_club().json()["id"]
    api_util.create_tag(name="test getter")

    assert client.get(f"/tag/1/").json()["name"] == "test getter"
    assert client.get(f"/tag/2/").json()["detail"] == "Tag not found"

    api_util.create_user2_and_authenticate()
    client.put(f"/club/{club_id}/join/")  # join the club
    assert client.get(f"/tag/1/").json()["name"] == "test getter"


def test_read_tags(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    club_id = api_util.create_club().json()["id"]
    api_util.create_tag(name="test getter")

    assert client.get(f"/tags/?club_id=1").json()["tags"][0]["name"] == "test getter"

    api_util.create_user2_and_authenticate()
    assert client.get(f"/tag/1/").json()["detail"] == "Tag not found"
    client.put(f"/club/{club_id}/join/")  # join the club
    assert client.get(f"/tag/1/").json()["name"] == "test getter"


def test_update_tag_and_archived_functionality(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    club_id = api_util.create_club().json()["id"]
    api_util.create_tag(name="test create")

    api_util.update_tag(tag_id=1, name="test update")
    assert client.get(f"/tag/1/").json()["name"] == "test update"
    assert api_util.update_tag(tag_id=1, archived=True)
    assert client.get(f"/tag/1/").json()["archived"] == True

    api_util.create_user2_and_authenticate()
    client.put(f"/club/{club_id}/join/")  # join the club as non admin member
    assert (
        api_util.update_tag(tag_id=1, name="invalid").json()["detail"]
        == "User not authorized to update tag"
    )

    assert not len(client.get(f"/tags/?club_id=1").json()["tags"])
    assert len(client.get(f"/tags/?club_id=1&archived=True").json()["tags"]) == 1


def test_delete_tag(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    club_id = api_util.create_club().json()["id"]
    api_util.create_tag(name="test create")

    client.delete("/tag/1/")
    assert client.get("/tag/1/").json()["detail"] == "Tag not found"

    api_util.create_tag(name="test create")
    api_util.create_user2_and_authenticate()
    client.put(f"/club/{club_id}/join/")  # join the club as non admin member

    assert (
        client.delete("/tag/1/").json()["detail"] == "User not authorized to delete tag"
    )
