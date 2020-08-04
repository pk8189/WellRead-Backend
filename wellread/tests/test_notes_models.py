from wellread.tests import utils


def test_create_read_update_delete_notes(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_team()
    no_user_res = api_util.create_note()
    assert no_user_res.status_code == 400
    slack_id_team = "AUSERPATRICK"
    api_util.create_user(slack_id_team_id=slack_id_team)
    no_club_res = api_util.create_note(slack_user_id=slack_id_team)
    assert no_club_res.status_code == 400
    club_id = api_util.create_club(admin_user_id=slack_id_team).json()["id"]
    delete_res = client.delete("/note/1/")
    assert delete_res.status_code == 400
    response = api_util.create_note(slack_user_id=slack_id_team)
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
        note_id=note_id, content="new content", private=True, archived=True
    )
    assert updated_res.status_code == 200, updated_res.text
    data = updated_res.json()
    assert data["content"] == "new content"
    assert data["private"] == True
    assert data["archived"] == True

    response = client.get(f"/note/?slack_id_team_id={slack_id_team}&club_id={club_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["notes"][0]["content"] == "new content"

    delete_res = client.delete(f"/note/{note_id}/")
    assert delete_res.status_code == 200, delete_res.text
    get_response = client.get(f"/note/{note_id}/")
    assert get_response.status_code == 400, get_response.text
    data = get_response.json()
    assert data["detail"] == "Note not found"

    response = api_util.create_note(slack_user_id=slack_id_team)
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

    client.delete(f"/club/1/")
    get_response = client.get(f"/note/{note_id}/")
    assert get_response.status_code == 400, get_response.text
