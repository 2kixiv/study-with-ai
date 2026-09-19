from app.exceptions import StudyTaskAlreadyCompletedError
from app.schemas import Priority, StudyTaskResponse


class StudyTaskRepository:
    """HTTP 및 비즈니스 규칙을 모르는 메모리 저장소입니다."""

    def __init__(self) -> None:
        self._tasks: dict[int, StudyTaskResponse] = {}
        self._next_id = 1

    def create(self, title: str, priority: Priority) -> StudyTaskResponse:
        task = StudyTaskResponse(
            id=self._next_id,
            title=title,
            priority=priority,
            completed=False
        )

        self._tasks.update({
            self._next_id : task
        })

        self._next_id += 1

        return task

    def list_all(self) -> list[StudyTaskResponse]:
        return list(self._tasks.values())

    def get(self, task_id: int) -> StudyTaskResponse | None:
        return self._tasks.get(task_id)

    def delete(self, task_id: int) -> bool:
        return self._tasks.pop(task_id, None) is not None

    def complete(self, task_id: int) -> StudyTaskResponse:
        task = self.get(task_id=task_id)

        if task.completed:
            raise StudyTaskAlreadyCompletedError()
        
        task.completed = True
        return task