from app.integration_tests import utils


def test_create_user(client):
    unauthenticated_res = client.get("/user/")  # make unauthenticated request to user
    assert unauthenticated_res.status_code == 401, unauthenticated_res.text
    assert unauthenticated_res.json()["detail"] == "Not authenticated"

    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    response = client.get("/user/")
    assert response.status_code == 200, response.text


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


def test_update_user(client):
    api_util = utils.MockApiRequests(client)
    api_util.create_user_and_authenticate()

    my_new_name = "Not Patrick Anymore!"
    new_email = "newemail@gmail.com"
    api_util.update_user(full_name=my_new_name, email=new_email)
    api_util.authenticate(email=new_email)

    data = client.get("/user/").json()
    assert data["full_name"] == my_new_name
    assert data["email"] == new_email
