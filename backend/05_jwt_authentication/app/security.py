from datetime import timedelta, datetime, timezone

import jwt
from pwdlib import PasswordHash

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY, JWT_ALGORITHM

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(
    user_id: int,
    expires_delta: timedelta | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    exp = now + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    access_token = jwt.encode({
        "sub": str(user_id),
        "iat": now,
        "exp": exp
    }, algorithm=JWT_ALGORITHM, key=JWT_SECRET_KEY)

    return access_token


def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, algorithms=JWT_ALGORITHM, key=JWT_SECRET_KEY)
    
    sub = payload.get("sub")

    if sub is None:
        raise jwt.InvalidTokenError()

    try:
        return int(sub)
    except:
        raise jwt.InvalidTokenError()