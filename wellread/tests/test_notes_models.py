from wellread.tests import utils


def test_create_read_update_delete_notes(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_team()
    no_user_res = api_util.create_note()
    assert no_user_res.status_code == 400
    api_util.create_user()
    no_club_res = api_util.create_note()
    assert no_club_res.status_code == 400
    api_util.create_club()
    delete_res = client.delete("/note/1/")
    assert delete_res.status_code == 400
    response = api_util.create_note()
    assert response.status_code == 200, response.text
    data = response.json()
    note_id = data["id"]
    assert data["content"] == "Oh my, such a lovely note!"
    get_response = client.get(f"/note/{note_id}/")
    assert get_response.status_code == 200, get_response.text
    data = get_response.json()
    assert data["content"] == "Oh my, such a lovely note!"
    updated_res = api_util.update_note(note_id=note_id, content="new content")
    assert updated_res.status_code == 200, updated_res.text
    data = updated_res.json()
    assert data["content"] == "new content"
    delete_res = client.delete(f"/note/{note_id}/")
    assert delete_res.status_code == 200, delete_res.text
    get_response = client.get(f"/note/{note_id}/")
    assert get_response.status_code == 400, get_response.text
    data = get_response.json()
    assert data["detail"] == "Note not found"

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
    assert updated_res.status_code == 200, updated_res.text
    data = updated_res.json()
    assert data["tags"] == tags
