import pytest
from fastapi.testclient import TestClient

import app.models  # ORM 모델을 Base metadata에 등록합니다.
from app.database import Base, engine
from app.main import app


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)

