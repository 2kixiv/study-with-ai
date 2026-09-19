from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repository import UserRepository
from app.service import UserService

DatabaseDependency = Annotated[Session, Depends(get_db)]


def get_repository(db: DatabaseDependency) -> UserRepository:
    return UserRepository(db)


RepositoryDependency = Annotated[UserRepository, Depends(get_repository)]


def get_service(repository: RepositoryDependency) -> UserService:
    return UserService(repository)


ServiceDependency = Annotated[UserService, Depends(get_service)]

