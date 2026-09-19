from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import StudyNote
from app.schemas import StudyNoteCreate


class StudyNoteRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, data: StudyNoteCreate) -> StudyNote:
        data_model = StudyNote(
            title=data.title,
            content=data.content
        )

        self._db.add(data_model)
        self._db.commit()
        self._db.refresh(data_model)

        return data_model

    def list_all(self) -> list[StudyNote]:
        stmt = select(StudyNote).order_by(StudyNote.id)
        result = self._db.scalars(statement=stmt)
        return list(result.all())

    def get(self, note_id: int) -> StudyNote | None:
        return self._db.get(StudyNote, note_id)

    def delete(self, note: StudyNote) -> None:
        self._db.delete(note)
        self._db.commit()