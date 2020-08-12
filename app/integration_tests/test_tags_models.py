from app.integration_tests import utils


def test_create_read_update_delete_tags(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()  # creates a user and authenticates the client

    response = api_util.create_tag()
    data = response.json()
    assert response.status_code == 400, response.text
    assert data["detail"] == "Club ID does not exist"

    club_id = api_util.create_club().json()["id"]
    response = api_util.create_tag(club_id=club_id, name="a new tag name")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "a new tag name"
    tag_id = data["id"]

    response = api_util.create_tag(club_id=club_id, name="a new tag name")
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Tag with this name already exists"

    response = client.get(f"/tag/{tag_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "a new tag name"

    response = client.get(f"/tag/?club_id={club_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["tags"][0]["name"] == "a new tag name"

    response = api_util.update_tag(tag_id=tag_id, name="newer name", archived=True)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "newer name"
    assert data["archived"] == True

    client.delete(f"/tag/{tag_id}/")
    response = client.get(f"/tag/{tag_id}/")
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Tag not found"

    response = client.delete(f"/tag/{tag_id}/")
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Tag not deleted, tag not found"
