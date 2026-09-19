import pytest
from fastapi.testclient import TestClient

from app.main import app, repository


@pytest.fixture(autouse=True)
def reset_repository() -> None:
    repository.clear()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

