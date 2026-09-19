from fastapi import APIRouter, Query, Response, status

from app.dependencies import ServiceDependency
from app.schemas import StudyTaskCreate, StudyTaskResponse

router = APIRouter(prefix="/api/v1/study-tasks", tags=["study-tasks"])


@router.post(
    "",
    response_model=StudyTaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    data: StudyTaskCreate, service: ServiceDependency
) -> StudyTaskResponse:
    return service.create(data=data)


@router.get("", response_model=list[StudyTaskResponse])
def list_tasks(
    service: ServiceDependency,
    completed: bool | None = Query(default=None),
) -> list[StudyTaskResponse]:
    return service.list_tasks(completed=completed)


@router.get("/{task_id}", response_model=StudyTaskResponse)
def get_task(task_id: int, service: ServiceDependency) -> StudyTaskResponse:
    return service.get(task_id=task_id)


@router.patch("/{task_id}/complete", response_model=StudyTaskResponse)
def complete_task(task_id: int, service: ServiceDependency) -> StudyTaskResponse:
    return service.complete(task_id=task_id)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_task(task_id: int, service: ServiceDependency) -> Response:
    service.delete(task_id=task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
