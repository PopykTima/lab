import pytest
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


@pytest.mark.asyncio
async def test_create_user(test_db_session: AsyncSession):
    user = User(name="Test User", email="user@test.com", age=25)
    test_db_session.add(user)
    await test_db_session.commit()
    await test_db_session.refresh(user)

    assert user.id is not None
    assert user.name == "Test User"
    assert user.email == "user@test.com"
    assert user.age == 25


@pytest.mark.asyncio
async def test_get_user_by_email(test_db_session: AsyncSession):
    user = User(name="John Doe", email="john@test.com", age=30)
    test_db_session.add(user)
    await test_db_session.commit()
    await test_db_session.refresh(user)

    result = await test_db_session.execute(select(User).where(User.email == "john@test.com"))
    found = result.scalars().first()

    assert found is not None
    assert found.id == user.id
    assert found.email == "john@test.com"


@pytest.mark.asyncio
async def test_update_user(test_db_session: AsyncSession):
    user = User(name="Old Name", email="old@test.com", age=20)
    test_db_session.add(user)
    await test_db_session.commit()
    await test_db_session.refresh(user)

    user.name = "New Name"
    user.age = 21
    await test_db_session.commit()
    await test_db_session.refresh(user)

    assert user.name == "New Name"
    assert user.age == 21


@pytest.mark.asyncio
async def test_delete_user(test_db_session: AsyncSession):
    user = User(name="Delete Me", email="delete@test.com", age=35)
    test_db_session.add(user)
    await test_db_session.commit()
    await test_db_session.refresh(user)

    user_id = user.id
    await test_db_session.delete(user)
    await test_db_session.commit()

    result = await test_db_session.execute(select(User).where(User.id == user_id))
    deleted = result.scalars().first()
    assert deleted is None
