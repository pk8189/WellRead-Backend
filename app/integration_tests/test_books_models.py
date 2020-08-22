from app.integration_tests import utils


def test_create_books(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    book_id = api_util.create_book(book_title="Meat", author_name="Is good").json()[
        "id"
    ]
    assert client.get(f"/api/book/{book_id}/").json()["book_title"] == "Meat"
    assert client.get(f"/api/book/{book_id}/").json()["author_name"] == "Is good"


def test_read_books(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    api_util.create_book(book_title="test1", author_name="itsame")
    assert client.get("/api/book/1/").json()["book_title"] == "test1"
    assert client.get("/api/book/1/").json()["author_name"] == "itsame"


def test_add_and_remove_book_from_user(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    book_id = api_util.create_book().json()["id"]

    client.put(f"/api/user/book/{book_id}/add/")
    assert len(client.get("/api/user/").json()["books"]) == 1
    assert len(client.get(f"/api/book/{book_id}/").json()["users"]) == 1

    client.put(f"/api/user/book/{book_id}/remove/")
    assert len(client.get("/api/user/").json()["books"]) == 0
    assert len(client.get(f"/api/book/{book_id}/").json()["users"]) == 0
