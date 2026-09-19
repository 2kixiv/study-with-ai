import pytest

from app.database import SessionLocal
from app.exceptions import DuplicateEmailError
from app.repository import UserRepository
from app.schemas import UserCreate


def test_duplicate_rolls_back_and_session_remains_usable() -> None:
    with SessionLocal() as session:
        repository = UserRepository(session)
        repository.create(UserCreate(email="same@example.com", name="first"))

        with pytest.raises(DuplicateEmailError):
            repository.create(UserCreate(email="same@example.com", name="duplicate"))

        created = repository.create(
            UserCreate(email="other@example.com", name="after rollback")
        )

    assert created.id == 3

