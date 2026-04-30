<<<<<<< HEAD
"""
Integration tests for API endpoints.
Tests HTTP endpoints with test database.
"""
import pytest
import pytest_asyncio
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(test_client: AsyncClient):
    """
    Test user registration endpoint.
    """
    # Arrange
    user_data = {
        "name": "New User",
        "email": "newuser@test.com",
        "age": 25,
        "password": "securepassword123"
    }
    
    # Act
    response = await test_client.post("/auth/register", json=user_data)
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New User"
    assert data["email"] == "newuser@test.com"
    assert data["age"] == 25
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(test_client: AsyncClient):
    """
    Test that duplicate email registration fails.
    """
    # Arrange - create first user
    user_data = {
        "name": "First User",
        "email": "duplicate@test.com",
        "age": 25,
        "password": "password123"
    }
    await test_client.post("/auth/register", json=user_data)
    
    # Act - try to register with same email
    response = await test_client.post("/auth/register", json=user_data)
    
    # Assert
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(test_client: AsyncClient):
    """
    Test successful user login.
    """
    # Arrange - create user first
    user_data = {
        "name": "Login User",
        "email": "login@test.com",
        "age": 30,
        "password": "mypassword123"
    }
    await test_client.post("/auth/register", json=user_data)
    
    # Act - login
    login_data = {
        "email": "login@test.com",
        "password": "mypassword123"
    }
    response = await test_client.post("/auth/login", json=login_data)
    
    # Assert
    assert response.status_code == 200
    # Login should set a cookie
    assert "set-cookie" in response.headers or response.cookies


@pytest.mark.asyncio
async def test_login_invalid_credentials(test_client: AsyncClient):
    """
    Test login with wrong password.
    """
    # Arrange - create user
    user_data = {
        "name": "Test User",
        "email": "loginfail@test.com",
        "age": 25,
        "password": "correctpassword"
    }
    await test_client.post("/auth/register", json=user_data)
    
    # Act - login with wrong password
    login_data = {
        "email": "loginfail@test.com",
        "password": "wrongpassword"
    }
    response = await test_client.post("/auth/login", json=login_data)
    
    # Assert
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_nonexistent_user(test_client: AsyncClient):
    """
    Test login with non-existent user.
    """
    # Act
    login_data = {
        "email": "nonexistent@test.com",
        "password": "anypassword"
    }
    response = await test_client.post("/auth/login", json=login_data)
    
    # Assert
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_endpoint_without_auth(test_client: AsyncClient):
    """
    Test accessing protected endpoint without authentication.
    """
    # Act - try to access protected endpoint (assuming there's one)
    # This test assumes there's a protected endpoint to test
    # Adjust the endpoint path based on your actual application
    
    # For now, test that unauthenticated requests are rejected
    # You would add actual protected endpoints to test
    pass


@pytest.mark.asyncio
async def test_register_invalid_email(test_client: AsyncClient):
    """
    Test registration with invalid email format.
    """
    # Act
    user_data = {
        "name": "Test User",
        "email": "not-an-email",
        "age": 25,
        "password": "password123"
    }
    response = await test_client.post("/auth/register", json=user_data)
    
    # Assert - Pydantic validation should fail
    assert response.status_code == 422  # FastAPI validation error


@pytest.mark.asyncio
async def test_register_missing_fields(test_client: AsyncClient):
    """
    Test registration with missing required fields.
    """
    # Act - missing age and password
    user_data = {
        "name": "Test User",
        "email": "test@example.com"
    }
    response = await test_client.post("/auth/register", json=user_data)
    
    # Assert
    assert response.status_code == 422
=======
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
>>>>>>> dev
