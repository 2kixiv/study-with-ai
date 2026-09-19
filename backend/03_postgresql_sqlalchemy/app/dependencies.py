from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repository import StudyNoteRepository
from app.service import StudyNoteService

DatabaseDependency = Annotated[Session, Depends(get_db)]


def get_repository(db: DatabaseDependency) -> StudyNoteRepository:
    return StudyNoteRepository(db)


RepositoryDependency = Annotated[StudyNoteRepository, Depends(get_repository)]


def get_service(repository: RepositoryDependency) -> StudyNoteService:
    return StudyNoteService(repository)


ServiceDependency = Annotated[StudyNoteService, Depends(get_service)]

