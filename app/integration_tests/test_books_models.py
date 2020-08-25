from app.integration_tests import utils


def test_create_books(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    book_id = api_util.create_book(
        google_books_id="aslkasdf", google_books_self_link="https://aasdf"
    ).json()["id"]
    assert client.get(f"/api/book/{book_id}/").json()["google_books_id"] == "aslkasdf"
    assert (
        client.get(f"/api/book/{book_id}/").json()["google_books_self_link"]
        == "https://aasdf"
    )

    api_util.create_user2_and_authenticate()
    book_id2 = api_util.create_book(
        google_books_id="aslkasdf", google_books_self_link="https://aasdf"
    ).json()["id"]
    assert book_id == book_id2


def test_read_books(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    first_res = client.get(f"/api/book/google_books/q=Harry+Potter").json()["volumes"][
        0
    ]
    api_util.create_book(
        google_books_id=first_res["id"], google_books_self_link=first_res["selfLink"]
    )

    google_book_id = client.get("/api/book/1/").json()["google_books_id"]
    assert client.get("/api/book/1/").json()["google_books_self_link"]
    assert client.get(f"/api/book/1/google_book/").json()["id"] == google_book_id


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


def test_google_books_query(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    query = "Harry+Potter"
    res = client.get(f"/api/book/google_books/q={query}").json()["volumes"]
    assert len(res)
