from app.exceptions import UserNotFoundError
from app.models import User
from app.repository import UserRepository
from app.schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def create(self, data: UserCreate) -> User:
        return self._repository.create(data)

    def list_users(
        self,
        *,
        is_active: bool | None,
        limit: int,
        offset: int,
    ) -> list[User]:
        return self._repository.list_all(
            is_active=is_active,
            limit=limit,
            offset=offset,
        )

    def get(self, user_id: int) -> User:
        user = self._repository.get(user_id)
        if user is None:
            raise UserNotFoundError
        return user

    def update(self, user_id: int, data: UserUpdate) -> User:
        user = self.get(user_id)
        return self._repository.update(user, data)

    def delete(self, user_id: int) -> None:
        user = self.get(user_id)
        self._repository.delete(user)

