from fastapi import APIRouter, Response, status

from app.dependencies import ServiceDependency
from app.schemas import StudyNoteCreate, StudyNoteResponse

router = APIRouter(prefix="/api/v1/notes", tags=["study-notes"])


@router.post(
    "",
    response_model=StudyNoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    data: StudyNoteCreate, service: ServiceDependency
) -> StudyNoteResponse:
    return service.create(data)


@router.get("", response_model=list[StudyNoteResponse])
def list_notes(service: ServiceDependency) -> list[StudyNoteResponse]:
    return service.list_notes()


@router.get("/{note_id}", response_model=StudyNoteResponse)
def get_note(note_id: int, service: ServiceDependency) -> StudyNoteResponse:
    return service.get(note_id)


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_note(note_id: int, service: ServiceDependency) -> Response:
    service.delete(note_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

