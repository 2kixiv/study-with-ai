from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import DuplicateEmailError
from app.models import User
from app.schemas import UserRegister


class UserRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, data: UserRegister, password_hash: str) -> User:
        try:
            user = User(
                email=data.email,
                name=data.name,
                password_hash=password_hash
            )
            self._db.add(user)
            self._db.commit()
            self._db.refresh(user)

            return user
        
        except IntegrityError as exc:
            self._db.rollback()
            raise DuplicateEmailError() from exc

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self._db.scalar(statement=stmt)

    def get(self, user_id: int) -> User | None:
        return self._db.get(User, user_id)

    def deactivate(self, user: User) -> User:
        user.is_active = False

        self._db.commit()
        self._db.refresh(user)

        return user
