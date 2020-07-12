def test_create_and_get_team(client):
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
            "team_id": "T0140PRK962",
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
