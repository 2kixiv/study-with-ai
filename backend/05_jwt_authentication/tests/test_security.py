from datetime import timedelta

import jwt
import pytest

from app.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_is_salted_and_verifiable() -> None:
    first = hash_password("same-password")
    second = hash_password("same-password")

    assert first != second
    assert verify_password("same-password", first) is True
    assert verify_password("wrong-password", first) is False


def test_decode_rejects_expired_and_invalid_subject() -> None:
    expired = create_access_token(1, expires_delta=timedelta(seconds=-1))

    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(expired)

    # 정상 서명 토큰이더라도 정수 사용자 ID가 아니면 거부해야 합니다.
    from app.config import JWT_ALGORITHM, JWT_SECRET_KEY

    invalid_subject = jwt.encode(
        {"sub": "not-an-integer"}, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
    )
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(invalid_subject)

