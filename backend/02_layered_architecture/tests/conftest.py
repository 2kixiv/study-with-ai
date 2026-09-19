import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_repository
from app.main import app
from app.repository import StudyTaskRepository


@pytest.fixture
def repository() -> StudyTaskRepository:
    return StudyTaskRepository()


@pytest.fixture
def client(repository: StudyTaskRepository):
    app.dependency_overrides[get_repository] = lambda: repository
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

