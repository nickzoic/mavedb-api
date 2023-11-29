from tempfile import TemporaryDirectory
from pathlib import Path
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mavedb.server_main import app
from mavedb.db.base import Base
from mavedb.deps import get_db
from mavedb.lib.authentication import get_current_user
from mavedb.models.user import User
from tests.helpers.constants import TEST_USER
from mavedb.db.session import engine, SessionLocal


local_session = SessionLocal()


@pytest.fixture()
def session():
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return local_session


def pytest_runtest_setup(item):
    local_session.begin()


def pytest_runtest_teardown(item):
    local_session.rollback()


@pytest.fixture()
def client(session):
    def override_current_user():
        default_user = session.query(User).filter(User.username == TEST_USER["username"]).one_or_none()
        yield default_user

    app.dependency_overrides[get_current_user] = override_current_user

    yield TestClient(app)
