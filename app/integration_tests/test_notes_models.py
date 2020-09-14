from app.integration_tests import utils


def test_create_note(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_book()

    response = api_util.create_note(content="test note")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["content"] == "test note"
    assert data["private"] == False
    assert data["archived"] == False


def test_read_note(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    note_id = api_util.create_note(content="test content").json()["id"]
    response = client.get(f"/api/note/{note_id}/")
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

    api_util.create_note(content="public_not_archived")

    for_archiving_id = api_util.create_note(content="test2").json()["id"]
    api_util.update_note(
        content="public_archived", note_id=for_archiving_id, archived=True
    )
    api_util.create_note(content="private_not_archived", private=True)
    private_for_archiving_id = api_util.create_note(
        content="test4", private=True
    ).json()["id"]
    api_util.update_note(
        content="private_archived",
        note_id=private_for_archiving_id,
        private=True,
        archived=True,
    )

    private_not_archived = client.get(f"/api/notes/me/?book_id=1").json()
    assert [note["content"] for note in private_not_archived["notes"]] == [
        "public_not_archived",
        "private_not_archived",
    ]

    public_including_archived_res = client.get(
        f"/api/notes/me/?book_id=1&include_archived=True"
    ).json()
    assert [note["content"] for note in public_including_archived_res["notes"]] == [
        "public_not_archived",
        "public_archived",
        "private_not_archived",
        "private_archived",
    ]

    public_not_including_archived_res = client.get(
        f"/api/notes/me/?book_id=1&include_private=False&include_archived=True"
    ).json()
    assert [note["content"] for note in public_not_including_archived_res["notes"]] == [
        "public_not_archived",
        "public_archived",
    ]


def test_add_tags_to_note(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    note_id = api_util.create_note(content="test1").json()["id"]
    tag_id = api_util.create_tag(name="testtag1").json()["id"]

    client.put(
        f"/api/note/{note_id}/tag/add/", json={"tags": [tag_id], "club_tags": []}
    )
    get_notes = client.get(f"/api/note/{note_id}/").json()
    assert get_notes["tags"][0]["name"] == "testtag1"

    get_tags = client.get(f"/api/tag/{tag_id}/").json()
    assert get_tags["name"] == "testtag1"

    invalid_tag_res = client.put(
        f"/api/note/{note_id}/tag/add/", json={"tags": [100], "club_tags": []}
    ).json()
    assert invalid_tag_res["detail"] == "Tag not found"

    invalid_note_res = client.put(
        f"/api/note/100/tag/", json={"tags": [1], "club_tags": []}
    ).json()
    assert invalid_note_res["detail"] == "Not Found"


def test_remove_tags_from_note(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    note_id = api_util.create_note(content="test1").json()["id"]
    tag_id = api_util.create_tag(name="testtag1").json()["id"]
    client.put(
        f"/api/note/{note_id}/tag/add/", json={"tags": [tag_id], "club_tags": []}
    )
    client.put(
        f"/api/note/{note_id}/tag/remove/", json={"tags": [tag_id], "club_tags": []}
    )
    assert not len(client.get(f"/api/note/{note_id}/").json()["tags"])


def test_delete_notes(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    note_id = api_util.create_note(content="test1").json()["id"]
    tag_id = api_util.create_tag(name="testtag1").json()["id"]
    client.put(
        f"/api/note/{note_id}/tag/add/", json={"tags": [tag_id], "club_tags": []}
    )

    client.delete(f"/api/note/{note_id}/")
    assert client.get(f"/api/note/{note_id}/").json()["detail"] == "Note not found"
    assert not client.get(f"/api/notes/club/?book_id=1").json().get("notes")
    assert not client.get(f"/api/tag/{tag_id}/").json().get("notes")

    user_1_note_id = api_util.create_note(content="test delete").json()["id"]

    api_util.create_user2_and_authenticate()  # create/login as another user
    assert (
        client.delete(f"/api/note/{user_1_note_id}/").json()["detail"]
        == "Note not found"
    )
