# Testing Guide

## Overview

This project includes unit and integration tests using **pytest** with async support.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py          # Test configuration (fixtures, setup/teardown)
├── test_repository.py   # Unit tests for database functions
└── test_api.py          # Integration tests for API endpoints
```

## Test Database

Tests use a separate PostgreSQL database (`app_test`) for isolation:

- **Production DB**: `app` (port 5432)
- **Test DB**: `app_test` (port 5433)

## Running Tests

### Prerequisites

1. Install test dependencies:

```bash
pip install pytest pytest-asyncio httpx
```

2. Start the test database:

```bash
docker-compose up -d db_test
```

### Run All Tests

```bash
pytest
```

### Run Specific Test Files

```bash
# Unit tests (repository layer)
pytest tests/test_repository.py

# Integration tests (API endpoints)
pytest tests/test_api.py
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

## Test Configuration

### conftest.py

Provides fixtures for:

- `test_engine` - Async database engine for test DB
- `test_db_session` - Database session with auto-cleanup
- `test_client` - HTTP client with overridden DB dependency

### Database Setup/Teardown

- **Setup**: Creates all tables before each test
- **Teardown**: Drops all tables after each test

This ensures test isolation - each test starts with a clean database.

## Dependency Injection

The test client uses FastAPI's dependency override:

```python
app.dependency_overrides[get_db] = override_get_db
```

This replaces the production database connection with the test session.

## Writing Tests

### Unit Test Example (test_repository.py)

```python
@pytest.mark.asyncio
async def test_create_user(test_db_session: AsyncSession):
    user = User(name="Test", email="test@test.com", ...)
    test_db_session.add(user)
    await test_db_session.commit()
    assert user.id is not None
```

### Integration Test Example (test_api.py)

```python
@pytest.mark.asyncio
async def test_register_user(test_client: AsyncClient):
    response = await test_client.post("/auth/register", json={
        "name": "Test",
        "email": "test@test.com",
        "age": 25,
        "password": "password123"
    })
    assert response.status_code == 200
```

## Docker Compose for Testing

The `docker-compose.yml` includes a `db_test` service:

```yaml
db_test:
  image: postgres:15
  environment:
    POSTGRES_DB: app_test
  ports:
    - "5433:5432"
```

Start only the test database:

```bash
docker-compose up -d db_test
```