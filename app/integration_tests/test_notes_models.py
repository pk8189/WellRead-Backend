from app.integration_tests import utils


def create_note(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    no_club_res = api_util.create_note()
    assert no_club_res.status_code == 400
    assert no_club_res.json()["detail"] == "Club ID does not exist"

    api_util.create_club().json()["id"]
    response = api_util.create_note()
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["content"] == "Oh my, such a lovely note!"
    assert data["private"] == False
    assert data["archived"] == False


def test_read_note(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    note_id = api_util.create_note(content="test content").json()["id"]
    response = client.get(f"/note/{note_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["content"] == "test content"


def test_update_note(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    note_id = api_util.create_note().json()[
        "id"
    ]  # defaults are private=False archived=False
    updated_res = api_util.update_note(
        note_id=note_id, content="test update", private=True, archived=True
    ).json()
    assert updated_res["content"] == "test update"
    assert updated_res["private"] == True
    assert updated_res["archived"] == True


def test_read_personal_notes(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    api_util.create_note(content="test1")
    for_archiving_id = api_util.create_note(content="test2").json()["id"]
    api_util.update_note(content="test2", note_id=for_archiving_id, archived=True)
    api_util.create_note(content="test3", private=True)
    private_for_archiving_id = api_util.create_note(
        content="test4", private=True
    ).json()["id"]
    api_util.update_note(
        content="test4", note_id=private_for_archiving_id, archived=True
    )

    public_non_archive_res = client.get(f"/notes/me/?club_id=1").json()
    assert len(public_non_archive_res["notes"]) == 1
    public_including_archived_res = client.get(
        f"/notes/me/?club_id=1&archived=True"
    ).json()
    assert [note["content"] for note in public_including_archived_res["notes"]] == [
        "test1",
        "test2",
        "test4",
    ]  # test3 is private
    including_private_and_non_archive_res = client.get(
        f"/notes/me/?club_id=1&private=True"
    ).json()
    assert [
        note["content"] for note in including_private_and_non_archive_res["notes"]
    ] == [
        "test1",
        "test3",
    ]  # test2 and test4 are archived
    including_private_and_archived_notes = client.get(
        f"/notes/me/?club_id=1&private=True&archived=True"
    ).json()
    assert [
        note["content"] for note in including_private_and_archived_notes["notes"]
    ] == ["test1", "test2", "test3", "test4"]


def test_read_team_notes(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    club_id = api_util.create_club().json()["id"]

    api_util.create_note(content="test1")
    api_util.create_note(content="shh it is private", private=True)

    api_util.create_user2_and_authenticate()
    client.put(f"/club/{club_id}/join/")  # join the club
    for_archiving_id = api_util.create_note(content="test2").json()["id"]
    api_util.update_note(content="test2", note_id=for_archiving_id, archived=True)

    shared_non_archive_res = client.get(f"/notes/club/?club_id=1").json()
    assert [note["content"] for note in shared_non_archive_res["notes"]] == ["test1"]
    shared_archive_res = client.get(f"/notes/club/?club_id=1&archived=True").json()
    assert [note["content"] for note in shared_archive_res["notes"]] == [
        "test1",
        "test2",
    ]


def test_add_tags_to_note(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    club_id = api_util.create_club().json()["id"]

    note_id = api_util.create_note(content="test1").json()["id"]
    tag_id = api_util.create_tag(name="testtag1").json()["id"]

    client.put(f"/note/{note_id}/tag/", json={"tags": [tag_id]})
    get_notes = client.get(f"/note/{note_id}/").json()
    assert get_notes["tags"][0]["name"] == "testtag1"
    get_tags = client.get(f"/tag/{tag_id}/").json()
    assert get_tags["name"] == "testtag1"

    invalid_tag_res = client.put(f"/note/{note_id}/tag/", json={"tags": [100]}).json()
    assert invalid_tag_res["detail"] == "Tag not found"

    invalid_note_res = client.put(f"/note/100/tag/", json={"tags": [1]}).json()
    assert invalid_note_res["detail"] == "Note not found"

    api_util.create_user2_and_authenticate()
    client.put(f"/club/{club_id}/join/")  # join the club
    another_user_tagging_notes = client.put(
        f"/note/{note_id}/tag/", json={"tags": [tag_id]}
    ).json()
    assert (
        another_user_tagging_notes["detail"]
        == "Unauthorized, user is not owner of note"
    )

    note_id = api_util.create_note(content="test2").json()["id"]
    client.put(f"/note/{note_id}/tag/", json={"tags": [tag_id]}).json()
    get_tag = client.get(f"/tag/{tag_id}/").json()
    assert len(get_tag["notes"]) == 2


def test_delete_notes(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    club_id = api_util.create_club().json()["id"]

    note_id = api_util.create_note(content="test1").json()["id"]
    tag_id = api_util.create_tag(name="testtag1").json()["id"]
    client.put(f"/note/{note_id}/tag/", json={"tags": [tag_id]})

    client.delete(f"/note/{note_id}/")
    assert client.get(f"/note/{note_id}/").json()["detail"] == "Note not found"
    assert not len(client.get(f"/notes/club/?club_id=1").json()["notes"])
    assert not len(client.get(f"/tag/{tag_id}/").json()["notes"])

    user_1_note_id = api_util.create_note(content="test delete").json()["id"]

    api_util.create_user2_and_authenticate()  # create/login as another user
    client.put(f"/club/{club_id}/join/")  # join the club

    assert (
        client.delete(f"/note/{user_1_note_id}/").json()["detail"]
        == "Unauthorized, user is not owner of note"
    )
