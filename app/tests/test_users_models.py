from app.tests import utils


def test_create_get_and_update_user(client):
    api_util = utils.MockApiRequests(client)

    response = api_util.create_user()
    assert response.status_code == 200, response.text
    data = response.json()
    user_id = data["id"]
    assert user_id == 1
    assert data["full_name"] == "Patrick M Kelly"

    response = client.get(f"/user/{user_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["full_name"] == "Patrick M Kelly"
    assert data["id"] == 1

    my_new_name = "Not Patrick Anymore!"
    response = api_util.update_user(user_id, full_name=my_new_name)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["full_name"] == my_new_name

    response = client.delete(f"/user/{user_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    response = client.get(f"/user/{id}/")
    data = response.json()
    assert response.status_code == 400, response.text
    assert data["detail"] == "User not found"
