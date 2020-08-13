from app.integration_tests import utils


def test_create_read_update_delete_notes(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()  # creates a user and authenticates the client

    no_club_res = api_util.create_note()
    assert no_club_res.status_code == 400  # club doesn't exist

    api_util.create_club().json()["id"]
    response = api_util.create_note()
    assert response.status_code == 200, response.text
    data = response.json()
    note_id = data["id"]
    assert data["content"] == "Oh my, such a lovely note!"
    assert data["private"] == False

    get_response = client.get(f"/note/{note_id}/")
    assert get_response.status_code == 200, get_response.text
    data = get_response.json()
    assert data["content"] == "Oh my, such a lovely note!"

    updated_res = api_util.update_note(
        note_id=note_id, content="new content", private=True
    )
    assert updated_res.status_code == 200, updated_res.text
    data = updated_res.json()
    assert data["content"] == "new content"
    assert data["private"] == True

    no_notes_because_private = client.get("/note/?club_id=1").json()
    assert not len(no_notes_because_private["notes"])
    api_util.update_note(
        note_id=note_id, content="new content", private=False, archived=True
    )
    no_notes_because_archived = client.get("/note/?club_id=1").json()
    assert not len(no_notes_because_archived["notes"])

    api_util.update_note(
        note_id=note_id, content="new content", private=False, archived=False
    )
    response = client.get("/note/?club_id=1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["notes"][0]["content"] == "new content"

    delete_res = client.delete(f"/note/{note_id}/")
    assert delete_res.status_code == 200, delete_res.text
    get_response = client.get(f"/note/{note_id}/")
    assert get_response.status_code == 400, get_response.text
    data = get_response.json()
    assert data["detail"] == "Note not found"

    data = api_util.create_note(private=True).json()  # create note as user 1
    user1s_note = data["id"]

    api_util.create_user2_and_authenticate()  # create and login as user 2
    data = client.get(f"/note/{note_id}/").json()
    assert data["detail"] == "Note not found"

    client.put(f"/club/1/join/")  # user 2 joins the club
    data = client.get(
        f"/note/{user1s_note}/"
    ).json()  # user 2 tries to get user 1s private note
    assert data["detail"] == "Not authorized"

    response = api_util.create_note()
    data = response.json()
    note_id = data["id"]
    response = api_util.create_tag()
    data = response.json()
    tag_id = data["id"]
    response = api_util.create_tag(name="second tag")
    data = response.json()
    tag_id_2 = data["id"]
    tags = [tag_id, tag_id_2]
    response = api_util.add_tags_to_note(note_id=note_id, tags=tags)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["tags"][0]["id"] == tags[0]
    assert data["tags"][1]["id"] == tags[1]
    response = client.get(f"/note/{note_id}/")
    data = response.json()
    assert len(data["tags"]) == 2

    api_util.authenticate()  # log back in as user 1
    client.delete(f"/club/1/")
    get_response = client.get(
        f"/note/{note_id}/"
    )  # note should not exist if club is deleted
    assert get_response.status_code == 400, get_response.text
    data = get_response.json()
    assert data["detail"] == "Note not found"
