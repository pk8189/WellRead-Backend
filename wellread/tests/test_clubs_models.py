def test_create_get_update_and_delete_club(client):
    # first create a team
    team_id = "T0140PRK962"
    response = client.post(
        "/team/",
        json={
            "team_id": team_id,
            "name": "WellRead",
            "domain": "www.domain.com",
            "email_domain": "",
        },
    )
    # create a user
    user_id = "U014YSCLQ2X_T0140PRK962"
    response = client.post(
        "/user/",
        json={
            "slack_id_team_id": user_id,
            "name": "Patrick K",
            "email": "pmkelly4444@gmail.com",
            "is_app_user": True,
            "is_owner": True,
            "locale": "ALocale",
            "profile_image_original": "https://localtiontosimage.com/test/",
            "team_id": team_id,
        },
    )
    # create a club for that team with the above user as admin
    book_title = "a big old book"
    response = client.post(
        "/club/",
        json={
            "book_title": book_title,
            "admin_user_id": user_id,
            "channel_id": "19WEWFJEW1425W",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"]
    assert data["book_title"] == book_title

    club_id = data["id"]
    response = client.get(f"/club/{club_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["channel_id"] == "19WEWFJEW1425W"
    assert data["admin_user_id"] == user_id
    assert not data["slack_users"]

    new_book_title = "Decolonizing Wealth"
    response = client.put(f"/club/{club_id}/", json={"book_title": new_book_title})
    assert response.status_code == 200, response.text
    response = client.get(f"/club/{club_id}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["book_title"] == new_book_title

    user_2 = "ALKAFKLJSDFKLJ"
    client.post(
        "/user/",
        json={
            "slack_id_team_id": user_2,
            "name": "User 2",
            "email": "anemail.gmail.com",
            "is_app_user": True,
            "is_owner": True,
            "locale": "ALocale",
            "profile_image_original": "https://localtiontosimage.com/test/",
            "team_id": team_id,
        },
    )

    response = client.put(f"/club/{club_id}/add_user/{user_2}/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["slack_users"][0]["slack_id_team_id"] == user_2

    response = client.delete(f"/club/{club_id}/")
    assert response.status_code == 200, response.text
    response = client.get(f"/club/{club_id}/")
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Club not found"
