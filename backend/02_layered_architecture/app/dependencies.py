from typing import Annotated

from fastapi import Depends

from app.repository import StudyTaskRepository
from app.service import StudyTaskService

_repository = StudyTaskRepository()


def get_repository() -> StudyTaskRepository:
    return _repository


def get_service(
    repository: Annotated[StudyTaskRepository, Depends(get_repository)],
) -> StudyTaskService:
    return StudyTaskService(repository=repository)


ServiceDependency = Annotated[StudyTaskService, Depends(get_service)]
