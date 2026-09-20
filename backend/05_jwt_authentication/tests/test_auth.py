from datetime import timedelta

import jwt
from fastapi.testclient import TestClient

from app.config import JWT_ALGORITHM, JWT_SECRET_KEY
from app.database import SessionLocal
from app.models import User
from app.security import create_access_token, verify_password


def register(
    client: TestClient,
    email: str = "user@example.com",
    password: str = "safe-password",
    name: str = "Learner",
):
    return client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "name": name},
    )


def login(
    client: TestClient,
    email: str = "user@example.com",
    password: str = "safe-password",
):
    return client.post(
        "/api/v1/auth/token",
        data={"username": email, "password": password},
    )


def bearer(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_register_hashes_password_and_never_returns_it(client: TestClient) -> None:
    response = register(client, email="  USER@Example.COM  ", name="  Kim  ")

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "user@example.com"
    assert body["name"] == "Kim"
    assert "password" not in body
    assert "password_hash" not in body

    with SessionLocal() as session:
        stored = session.get(User, body["id"])
        assert stored is not None
        assert stored.password_hash != "safe-password"
        assert verify_password("safe-password", stored.password_hash) is True


def test_register_validates_input(client: TestClient) -> None:
    invalid_payloads = [
        {"email": "invalid", "name": "name", "password": "safe-password"},
        {"email": "a@b.com", "name": " ", "password": "safe-password"},
        {"email": "a@b.com", "name": "name", "password": "short"},
        {"email": "a@b.com", "name": "name", "password": "x" * 129},
        {"email": "a@b.com", "name": "name", "password": "safe-password", "admin": True},
    ]
    for payload in invalid_payloads:
        assert client.post("/api/v1/auth/register", json=payload).status_code == 422


def test_duplicate_email_returns_409(client: TestClient) -> None:
    assert register(client).status_code == 201
    response = register(client, email="USER@example.com")

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already exists"}


def test_login_returns_signed_jwt_with_required_claims(client: TestClient) -> None:
    user = register(client).json()

    response = login(client, email=" USER@EXAMPLE.COM ")

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    token = response.json()["access_token"]
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    assert payload["sub"] == str(user["id"])
    assert "iat" in payload
    assert "exp" in payload


def test_login_uses_same_error_for_unknown_email_and_wrong_password(
    client: TestClient,
) -> None:
    register(client)

    unknown = login(client, email="missing@example.com")
    wrong = login(client, password="wrong-password")

    assert unknown.status_code == 401
    assert wrong.status_code == 401
    assert unknown.json() == wrong.json() == {"detail": "Invalid credentials"}
    assert unknown.headers["www-authenticate"] == "Bearer"


def test_me_requires_valid_token(client: TestClient) -> None:
    missing = client.get("/api/v1/users/me")
    malformed = client.get("/api/v1/users/me", headers=bearer("not-a-jwt"))
    expired = client.get(
        "/api/v1/users/me",
        headers=bearer(create_access_token(1, expires_delta=timedelta(seconds=-1))),
    )

    assert missing.status_code == 401
    assert malformed.status_code == 401
    assert expired.status_code == 401


def test_me_returns_authenticated_user(client: TestClient) -> None:
    registered = register(client).json()
    token = login(client).json()["access_token"]

    response = client.get("/api/v1/users/me", headers=bearer(token))

    assert response.status_code == 200
    assert response.json() == registered


def test_deactivated_user_is_forbidden_with_existing_token(client: TestClient) -> None:
    register(client)
    token = login(client).json()["access_token"]

    deactivated = client.post(
        "/api/v1/users/me/deactivate", headers=bearer(token)
    )
    retried = client.get("/api/v1/users/me", headers=bearer(token))

    assert deactivated.status_code == 200
    assert deactivated.json()["is_active"] is False
    assert retried.status_code == 403
    assert retried.json() == {"detail": "Inactive user"}

