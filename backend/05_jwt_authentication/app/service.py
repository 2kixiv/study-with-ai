from app.exceptions import InvalidCredentialsError
from app.models import User
from app.repository import UserRepository
from app.schemas import UserRegister
from app.security import hash_password, verify_password


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def register(self, data: UserRegister) -> User:
        hashed_password = hash_password(data.password)
        return self._repository.create(data, hashed_password)

    def authenticate(self, email: str, password: str) -> User:
        user = self._repository.get_by_email(email.strip().lower())

        if user is None:
            raise InvalidCredentialsError()
        
        is_verified = verify_password(password, user.password_hash)

        if not is_verified:
            raise InvalidCredentialsError()

        return user

    def get_user(self, user_id: int) -> User | None:
        return self._repository.get(user_id)

    def deactivate(self, user: User) -> User:
        user = self._repository.deactivate(user)
        return user
