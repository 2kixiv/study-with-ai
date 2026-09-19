from app.exceptions import (
    DuplicateActiveTaskError,
    StudyTaskAlreadyCompletedError,
    StudyTaskNotFoundError,
)
from app.repository import StudyTaskRepository
from app.schemas import StudyTaskCreate, StudyTaskResponse


class StudyTaskService:
    """학습 할 일의 유스케이스와 비즈니스 규칙을 담당합니다."""

    def __init__(self, repository: StudyTaskRepository) -> None:
        self._repository = repository

    def create(self, data: StudyTaskCreate) -> StudyTaskResponse:
        tasks = self._repository.list_all()

        for task in [task for task in tasks if not task.completed]:
            if task.title.casefold() == data.title.casefold():
                raise DuplicateActiveTaskError()

        return self._repository.create(data.title, data.priority)

    def list_tasks(self, completed: bool | None = None) -> list[StudyTaskResponse]:
        if completed is None:
            return self._repository.list_all()

        tasks = self._repository.list_all()
        return [task for task in tasks if task.completed == completed]

    def get(self, task_id: int) -> StudyTaskResponse:
        task = self._repository.get(task_id=task_id)

        if task is None:
            raise StudyTaskNotFoundError()

        return task

    def complete(self, task_id: int) -> StudyTaskResponse:
        task = self._repository.get(task_id=task_id)

        if task is None:
            raise StudyTaskNotFoundError()

        if task.completed:
            raise StudyTaskAlreadyCompletedError()

        return self._repository.complete(task_id=task_id)

    def delete(self, task_id: int) -> None:
        is_deleted = self._repository.delete(task_id=task_id)

        if not is_deleted:
            raise StudyTaskNotFoundError()