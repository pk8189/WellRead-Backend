from wellread.tests import utils


def test_create_read_update_delete_tags(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_team()
    api_util.create_user()

    response = api_util.create_tag()
    data = response.json()
    assert response.status_code == 400, response.text
    assert data["detail"] == "Club ID does not exist"

    slack_club_id = api_util.create_club().json()["id"]
    response = api_util.create_tag(slack_club_id=slack_club_id, name="a new tag name")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "a new tag name"
    tag_id = data["id"]

    response = api_util.create_tag(slack_club_id=slack_club_id, name="a new tag name")
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Tag already exists"

    response = client.get(f"/tag/{tag_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "a new tag name"

    response = client.get(f"/tag/?club_id={slack_club_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["tags"][0]["name"] == "a new tag name"

    response = api_util.update_tag(tag_id=tag_id, name="newer name")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "newer name"

    client.delete(f"/tag/{tag_id}/")
    response = client.get(f"/tag/{tag_id}/")
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Tag not found"

    response = client.delete(f"/tag/{tag_id}/")
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Tag not deleted, tag not found"
