import pytest


@pytest.mark.asyncio
async def test_create_user(client):

    payload = {
        "name": "John Doe",
        "email": "john@test.com"
    }

    response = await client.post("/users/", json=payload)

    assert response.status_code == 201

    body = response.json()

    assert body["name"] == payload["name"]
    assert body["email"] == payload["email"]
    assert "id" in body


@pytest.mark.asyncio
async def test_get_users(client):

    await client.post("/users/", json={
        "name": "Jane Hill",
        "email": "jane@test.com"
    })

    response = await client.get("/users/")

    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_get_user_by_id(client):

    create = await client.post("/users/", json={
        "name": "Noelle Lee",
        "email": "noelle@test.com"
    })

    user_id = create.json()["id"]

    response = await client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id


@pytest.mark.asyncio
async def test_update_user(client):

    create = await client.post("/users/", json={
        "name": "Bob Sam",
        "email": "bob@test.com"
    })

    user_id = create.json()["id"]

    update = await client.put(
        f"/users/{user_id}",
        json={"name": "New Name"}
    )

    assert update.status_code == 200
    assert update.json()["name"] == "New Name"


@pytest.mark.asyncio
async def test_delete_user(client):

    create = await client.post("/users/", json={
        "name": "Delete Me",
        "email": "delete@test.com"
    })

    user_id = create.json()["id"]

    delete = await client.delete(f"/users/{user_id}")

    assert delete.status_code == 204

    check = await client.get(f"/users/{user_id}")
    assert check.status_code == 404
