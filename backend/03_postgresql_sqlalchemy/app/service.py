from app.exceptions import StudyNoteNotFoundError
from app.models import StudyNote
from app.repository import StudyNoteRepository
from app.schemas import StudyNoteCreate


class StudyNoteService:
    def __init__(self, repository: StudyNoteRepository) -> None:
        self._repository = repository

    def create(self, data: StudyNoteCreate) -> StudyNote:
        return self._repository.create(data)

    def list_notes(self) -> list[StudyNote]:
        return self._repository.list_all()

    def get(self, note_id: int) -> StudyNote:
        note = self._repository.get(note_id)
        if note is None:
            raise StudyNoteNotFoundError
        return note

    def delete(self, note_id: int) -> None:
        note = self.get(note_id)
        self._repository.delete(note)

