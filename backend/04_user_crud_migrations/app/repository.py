from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import DuplicateEmailError
from app.models import User
from app.schemas import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, data: UserCreate) -> User:
        user = User(
            email=data.email,
            name=data.name
        )

        try:
            self._db.add(user)
            self._db.commit()
            self._db.refresh(user)
        except IntegrityError as exc:
            self._db.rollback()
            raise DuplicateEmailError() from exc

        return user

    def list_all(
        self,
        *,
        is_active: bool | None,
        limit: int,
        offset: int,
    ) -> list[User]:
        stmt = select(User)

        if is_active is not None:
            stmt = stmt.where(User.is_active == is_active)

        stmt = (
            stmt.order_by(User.id)
                .offset(offset=offset)
                .limit(limit=limit)
        )

        users = self._db.scalars(statement=stmt).all()

        return users

    def get(self, user_id: int) -> User | None:
        user = self._db.get(User, user_id)
        return user

    def update(self, user: User, data: UserUpdate) -> User:
        if data.name is not None:
            user.name = data.name

        if data.is_active is not None:
            user.is_active = data.is_active

        self._db.commit()
        self._db.refresh(user)

        return user

    def delete(self, user: User) -> None:
        self._db.delete(user)
        self._db.commit()
