from app.integration_tests import utils


def test_create_user(client):
    unauthenticated_res = client.get("/user/")  # make unauthenticated request to user
    assert unauthenticated_res.status_code == 401, unauthenticated_res.text
    assert unauthenticated_res.json()["detail"] == "Not authenticated"

    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    response = client.get("/user/")
    assert response.status_code == 200, response.text

    assert (
        client.post(
            "/token", data={"username": "pmkelly4444@gmail.com", "password": "1"}
        ).json()["detail"]
        == "Incorrect username or password"
    )

    assert (
        client.post(
            "/token", data={"username": "invalid", "password": "string"}
        ).json()["detail"]
        == "Incorrect username or password"
    )


def test_get_user(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    data = client.get("/user/").json()
    assert data["full_name"] == "Patrick M Kelly"  # default user full name
    assert data["id"] == 1  # first ID
    assert data["email"] == "pmkelly4444@gmail.com"  # default email
    assert not data.get("password") and not data.get(
        "hashed_password"
    )  # make sure password is never sent
