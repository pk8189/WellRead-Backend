from app.integration_tests import utils


def test_create_tag(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    response = api_util.create_tag(name="a new tag name")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "a new tag name"


def test_read_tag(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_tag(name="test getter")

    assert client.get(f"/tag/1/").json()["name"] == "test getter"
    assert client.get(f"/tag/2/").json()["detail"] == "Tag not found"


def test_read_tags(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_tag(name="test getter")

    assert client.get(f"/tags/?club_id=1").json()["tags"][0]["name"] == "test getter"


def test_update_tag_and_archived_functionality(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_tag(name="test create")

    api_util.update_tag(tag_id=1, name="test update")
    assert client.get(f"/tag/1/").json()["name"] == "test update"
    assert api_util.update_tag(tag_id=1, archived=True)
    assert client.get(f"/tag/1/").json()["archived"] == True


def test_delete_tag(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_tag(name="test create")

    client.delete("/tag/1/")
    assert client.get("/tag/1/").json()["detail"] == "Tag not found"
