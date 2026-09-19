from collections.abc import Generator

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import inspect, text

from app.database import engine
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def apply_migrations() -> Generator[None, None, None]:
    config = Config("alembic.ini")
    command.downgrade(config, "base")
    command.upgrade(config, "head")
    yield
    command.downgrade(config, "base")


@pytest.fixture(autouse=True)
def clean_users_table() -> None:
    if inspect(engine).has_table("users"):
        with engine.begin() as connection:
            connection.execute(text("TRUNCATE TABLE users RESTART IDENTITY"))


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

