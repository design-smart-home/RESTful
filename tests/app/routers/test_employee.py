async def test_post_user(client, db_session):
    response = await client.post("/employee", json={
        "login": "test",
        "password": "test",
        "salary": 1000000,
        "date_of_promotion": "23-10-2025"
    })

    assert response.status_code == 201