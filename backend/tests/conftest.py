import pytest
from fastapi.testclient import TestClient

from ..main import app
from ..models import get_session
from ..utils import TokenType, create_access_token, create_refresh_token
from .db import create_tables, drop_tables
from .db import get_session as test_get_session
from .db import insert_users


@pytest.fixture(scope="function")
def client():
    app.dependency_overrides[get_session] = test_get_session

    drop_tables()
    create_tables()

    insert_users()

    with TestClient(app) as client:
        yield client

    drop_tables()


@pytest.fixture
def user_access_token():
    return create_access_token("1")


@pytest.fixture
def user_refresh_token():
    return create_refresh_token("1")


@pytest.fixture
def admin_access_token():
    return create_access_token("1", is_admin=True)


@pytest.fixture
def admin_refresh_token():
    return create_refresh_token("1", is_admin=True)


@pytest.fixture
def token_type():
    return TokenType
