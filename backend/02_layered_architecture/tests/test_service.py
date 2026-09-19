import pytest

from app.exceptions import (
    DuplicateActiveTaskError,
    StudyTaskAlreadyCompletedError,
    StudyTaskNotFoundError,
)
from app.repository import StudyTaskRepository
from app.schemas import Priority, StudyTaskCreate
from app.service import StudyTaskService


@pytest.fixture
def service() -> StudyTaskService:
    return StudyTaskService(StudyTaskRepository())


def test_service_enforces_duplicate_rule(service: StudyTaskService) -> None:
    service.create(StudyTaskCreate(title="Repository", priority=Priority.LOW))

    with pytest.raises(DuplicateActiveTaskError):
        service.create(StudyTaskCreate(title="repository", priority=Priority.HIGH))


def test_service_raises_domain_errors(service: StudyTaskService) -> None:
    with pytest.raises(StudyTaskNotFoundError):
        service.get(999)

    task = service.create(StudyTaskCreate(title="Exceptions"))
    service.complete(task.id)

    with pytest.raises(StudyTaskAlreadyCompletedError):
        service.complete(task.id)

