from typing import Annotated
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.auth import AuthRepository, decode_access_token
from app.database import get_db
from app.exceptions import InactiveUserError, InvalidCredentialsError
from app.models import User
from app.post_repository import PostRepository
from app.post_service import PostService

DatabaseDependency = Annotated[Session, Depends(get_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def get_auth_repository(db: DatabaseDependency) -> AuthRepository:
    return AuthRepository(db)


AuthRepositoryDependency = Annotated[AuthRepository, Depends(get_auth_repository)]


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: DatabaseDependency) -> User:
    try:
        user_id = decode_access_token(token)
    except jwt.InvalidTokenError as exc:
        raise InvalidCredentialsError from exc
    user = db.get(User, user_id)
    if user is None:
        raise InvalidCredentialsError
    if not user.is_active:
        raise InactiveUserError
    return user


ActiveUserDependency = Annotated[User, Depends(get_current_user)]


def get_post_repository(db: DatabaseDependency) -> PostRepository:
    return PostRepository(db)


PostRepositoryDependency = Annotated[PostRepository, Depends(get_post_repository)]


def get_post_service(repository: PostRepositoryDependency) -> PostService:
    return PostService(repository)


PostServiceDependency = Annotated[PostService, Depends(get_post_service)]

