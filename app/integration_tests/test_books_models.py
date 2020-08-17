from app.integration_tests import utils


def test_create_books(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    book_id = api_util.create_book().json()["id"]
    assert client.get(f"/book/{book_id}/").json()["book_title"]


def test_read_books(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    api_util.create_book(book_title="test1", author_name="itsame", club_id=1)
    assert client.get("/book/1/").json()["book_title"] == "test1"
    assert client.get("/book/1/").json()["author_name"] == "itsame"
    assert client.get("/book/1/").json()["archived"] == False


def test_update_books(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()
    api_util.create_book()

    api_util.update_book(
        archived=True, book_title="test1", author_name="itsame",
    )
    assert client.get("/book/1/").json()["book_title"] == "test1"
    assert client.get("/book/1/").json()["author_name"] == "itsame"
    assert client.get("/book/1/").json()["archived"] == True


def test_delete_books(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()
    api_util.create_club()

    book_id = api_util.create_book().json()["id"]

    client.delete(f"/book/{book_id}/")
    assert not client.get("/book/1/").json()
