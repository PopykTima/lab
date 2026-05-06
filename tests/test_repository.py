"""
Unit tests for database repository functions.
Tests User CRUD operations with isolated test database.
"""
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import User
from app.security import get_password_hash, verify_password


@pytest.mark.asyncio
async def test_create_user(test_db_session: AsyncSession):
    """
    Test creating a new user in the database.
    """
    # Arrange
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "age": 25,
        "hashed_password": get_password_hash("password123")
    }
    
    # Act
    new_user = User(**user_data)
    test_db_session.add(new_user)
    await test_db_session.commit()
    await test_db_session.refresh(new_user)
    
    # Assert
    assert new_user.id is not None
    assert new_user.name == "Test User"
    assert new_user.email == "test@example.com"
    assert new_user.age == 25
    assert verify_password("password123", new_user.hashed_password)


@pytest.mark.asyncio
async def test_get_user_by_email(test_db_session: AsyncSession):
    """
    Test retrieving a user by email address.
    """
    # Arrange - create user first
    user = User(
        name="John Doe",
        email="john@example.com",
        age=30,
        hashed_password=get_password_hash("secret123")
    )
    test_db_session.add(user)
    await test_db_session.commit()
    await test_db_session.refresh(user)
    
    # Act - query user by email
    result = await test_db_session.execute(
        select(User).where(User.email == "john@example.com")
    )
    found_user = result.scalars().first()
    
    # Assert
    assert found_user is not None
    assert found_user.id == user.id
    assert found_user.name == "John Doe"


@pytest.mark.asyncio
async def test_get_user_by_id(test_db_session: AsyncSession):
    """
    Test retrieving a user by ID.
    """
    # Arrange
    user = User(
        name="Jane Doe",
        email="jane@example.com",
        age=28,
        hashed_password=get_password_hash("password456")
    )
    test_db_session.add(user)
    await test_db_session.commit()
    await test_db_session.refresh(user)
    user_id = user.id
    
    # Act
    result = await test_db_session.execute(
        select(User).where(User.id == user_id)
    )
    found_user = result.scalars().first()
    
    # Assert
    assert found_user is not None
    assert found_user.email == "jane@example.com"


@pytest.mark.asyncio
async def test_update_user(test_db_session: AsyncSession):
    """
    Test updating a user's information.
    """
    # Arrange
    user = User(
        name="Old Name",
        email="old@example.com",
        age=20,
        hashed_password=get_password_hash("oldpassword")
    )
    test_db_session.add(user)
    await test_db_session.commit()
    await test_db_session.refresh(user)
    
    # Act
    user.name = "New Name"
    user.age = 21
    await test_db_session.commit()
    await test_db_session.refresh(user)
    
    # Assert
    assert user.name == "New Name"
    assert user.age == 21


@pytest.mark.asyncio
async def test_delete_user(test_db_session: AsyncSession):
    """
    Test deleting a user from the database.
    """
    # Arrange
    user = User(
        name="To Delete",
        email="delete@example.com",
        age=35,
        hashed_password=get_password_hash("delpass")
    )
    test_db_session.add(user)
    await test_db_session.commit()
    await test_db_session.refresh(user)
    user_id = user.id
    
    # Act
    await test_db_session.delete(user)
    await test_db_session.commit()
    
    # Assert - verify user is deleted
    result = await test_db_session.execute(
        select(User).where(User.id == user_id)
    )
    deleted_user = result.scalars().first()
    assert deleted_user is None


@pytest.mark.asyncio
async def test_user_email_unique_constraint(test_db_session: AsyncSession):
    """
    Test that email must be unique.
    """
    # Arrange - create first user
    user1 = User(
        name="First User",
        email="unique@example.com",
        age=25,
        hashed_password=get_password_hash("password1")
    )
    test_db_session.add(user1)
    await test_db_session.commit()
    
    # Act - try to create second user with same email
    user2 = User(
        name="Second User",
        email="unique@example.com",  # Same email
        age=30,
        hashed_password=get_password_hash("password2")
    )
    test_db_session.add(user2)
    
    # Assert - should raise integrity error
    with pytest.raises(Exception):  # IntegrityError
        await test_db_session.commit()
