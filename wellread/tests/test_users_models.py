def test_create_get_and_update_user(client):
    team_id = "T0140PRK962"
    response = client.post(
        "/user/",
        json={
            "slack_id_team_id": "U014YSCLQ2X_T0140PRK962",
            "name": "Patrick K",
            "email": "pmkelly4444@gmail.com",
            "is_app_user": True,
            "is_owner": True,
            "locale": "ALocale",
            "profile_image_original": "https://localtiontosimage.com/test/",
            "team_id": team_id,
        },
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == f"No team exists for specified team_id: {team_id}"

    response = client.post(
        "/team/",
        json={
            "team_id": team_id,
            "name": "WellRead",
            "domain": "www.domain.com",
            "email_domain": "",
        },
    )
    assert response.status_code == 200, response.text

    response = client.post(
        "/user/",
        json={
            "slack_id_team_id": "U014YSCLQ2X_T0140PRK962",
            "name": "Patrick K",
            "email": "pmkelly4444@gmail.com",
            "is_app_user": True,
            "is_owner": True,
            "locale": "ALocale",
            "profile_image_original": "https://localtiontosimage.com/test/",
            "team_id": team_id,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    slack_id_team_id = data["slack_id_team_id"]
    assert slack_id_team_id == "U014YSCLQ2X_T0140PRK962"
    assert data["name"] == "Patrick K"

    response = client.get(f"/user/{slack_id_team_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Patrick K"
    assert data["slack_id_team_id"] == "U014YSCLQ2X_T0140PRK962"

    my_new_name = "Not Patrick Anymore!"
    response = client.put(
        f"/user/{slack_id_team_id}/", json={"name": my_new_name, "is_owner": False,},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == my_new_name
    assert data["is_owner"] == False

    response = client.delete(f"/user/{slack_id_team_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["slack_id_team_id"] == slack_id_team_id
    response = client.get(f"/user/{slack_id_team_id}/")
    data = response.json()
    assert response.status_code == 400, response.text
    assert data["detail"] == "User not found"
