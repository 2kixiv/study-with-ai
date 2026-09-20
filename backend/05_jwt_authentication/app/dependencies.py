from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import InactiveUserError, InvalidCredentialsError
from app.models import User
from app.repository import UserRepository
from app.security import decode_access_token
from app.service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

DatabaseDependency = Annotated[Session, Depends(get_db)]


def get_repository(db: DatabaseDependency) -> UserRepository:
    return UserRepository(db)


RepositoryDependency = Annotated[UserRepository, Depends(get_repository)]


def get_service(repository: RepositoryDependency) -> AuthService:
    return AuthService(repository)


ServiceDependency = Annotated[AuthService, Depends(get_service)]
TokenDependency = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(
    token: TokenDependency,
    service: ServiceDependency,
) -> User:
    try:
        user_id = decode_access_token(token)
    except:
        raise InvalidCredentialsError()
    
    user = service.get_user(user_id=user_id)

    if user is None:
        raise InvalidCredentialsError()

    return user


CurrentUserDependency = Annotated[User, Depends(get_current_user)]


def get_current_active_user(user: CurrentUserDependency) -> User:
    if not user.is_active:
        raise InactiveUserError()

    return user


ActiveUserDependency = Annotated[User, Depends(get_current_active_user)]
