from datetime import UTC, datetime, timedelta
import jwt
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY
from app.exceptions import DuplicateEmailError, InvalidCredentialsError
from app.models import User

password_hash = PasswordHash.recommended()


def hash_password(value: str) -> str:
    return password_hash.hash(value)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


def create_access_token(user_id: int) -> str:
    now = datetime.now(UTC)
    return jwt.encode({"sub": str(user_id), "iat": now, "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    try:
        return int(payload["sub"])
    except (KeyError, TypeError, ValueError) as exc:
        raise jwt.InvalidTokenError("Invalid subject") from exc


class AuthRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def register(self, email: str, name: str, password: str) -> User:
        user = User(email=email, name=name, password_hash=hash_password(password))
        self.db.add(user)
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise DuplicateEmailError from exc
        self.db.refresh(user)
        return user

    def authenticate(self, email: str, password: str) -> User:
        user = self.db.scalar(select(User).where(User.email == email.strip().lower()))
        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError
        return user

