import pytest


@pytest.mark.asyncio
async def test_create_user_endpoint(test_client):
    payload = {
        "name": "API User",
        "email": "apiuser@test.com",
        "age": 28,
    }
    response = await test_client.post("/users/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "API User"
    assert data["email"] == "apiuser@test.com"
    assert data["age"] == 28


@pytest.mark.asyncio
async def test_get_users_endpoint(test_client):
    payload = {
        "name": "List User",
        "email": "listuser@test.com",
        "age": 30,
    }
    await test_client.post("/users/", json=payload)

    response = await test_client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(user["email"] == "listuser@test.com" for user in data)
