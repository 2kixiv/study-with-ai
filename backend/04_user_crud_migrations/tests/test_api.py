from fastapi.testclient import TestClient


def create_user(
    client: TestClient,
    email: str = "learner@example.com",
    name: str = "Learner",
):
    return client.post("/api/v1/users", json={"email": email, "name": name})


def test_create_user_normalizes_email_and_uses_database_defaults(
    client: TestClient,
) -> None:
    response = create_user(client, email="  USER@Example.COM  ", name="  Kim  ")

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "email": "user@example.com",
        "name": "Kim",
        "is_active": True,
        "created_at": response.json()["created_at"],
        "updated_at": response.json()["updated_at"],
    }
    assert response.json()["created_at"] is not None
    assert response.json()["updated_at"] is not None


def test_create_user_validates_input(client: TestClient) -> None:
    invalid_payloads = [
        {"email": "not-an-email", "name": "valid"},
        {"email": "user@example.com", "name": "   "},
        {"email": "user@example.com", "name": "a" * 51},
        {"email": "user@example.com", "name": "valid", "unknown": True},
    ]

    for payload in invalid_payloads:
        response = client.post("/api/v1/users", json=payload)
        assert response.status_code == 422, payload


def test_duplicate_email_returns_conflict(client: TestClient) -> None:
    assert create_user(client, email="user@example.com").status_code == 201

    duplicate = create_user(client, email="USER@example.com")

    assert duplicate.status_code == 409
    assert duplicate.json() == {"detail": "Email already exists"}


def test_list_users_filters_and_paginates(client: TestClient) -> None:
    first = create_user(client, "first@example.com", "first").json()
    second = create_user(client, "second@example.com", "second").json()
    create_user(client, "third@example.com", "third")
    client.patch(f"/api/v1/users/{second['id']}", json={"is_active": False})

    paged = client.get("/api/v1/users?limit=1&offset=1")
    active = client.get("/api/v1/users?is_active=true")
    inactive = client.get("/api/v1/users?is_active=false")

    assert [user["name"] for user in paged.json()] == ["second"]
    assert [user["name"] for user in active.json()] == ["first", "third"]
    assert [user["name"] for user in inactive.json()] == ["second"]
    assert first["id"] == 1


def test_get_user_and_missing_user(client: TestClient) -> None:
    created = create_user(client).json()

    found = client.get(f"/api/v1/users/{created['id']}")
    missing = client.get("/api/v1/users/999")

    assert found.status_code == 200
    assert found.json() == created
    assert missing.status_code == 404
    assert missing.json() == {"detail": "User not found"}


def test_patch_updates_only_sent_fields(client: TestClient) -> None:
    created = create_user(client).json()

    response = client.patch(
        f"/api/v1/users/{created['id']}", json={"name": "Updated"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated"
    assert response.json()["email"] == created["email"]
    assert response.json()["is_active"] is True


def test_patch_requires_a_field_and_existing_user(client: TestClient) -> None:
    user_id = create_user(client).json()["id"]

    empty = client.patch(f"/api/v1/users/{user_id}", json={})
    missing = client.patch("/api/v1/users/999", json={"name": "Updated"})

    assert empty.status_code == 422
    assert missing.status_code == 404


def test_delete_user(client: TestClient) -> None:
    user_id = create_user(client).json()["id"]

    deleted = client.delete(f"/api/v1/users/{user_id}")
    fetched = client.get(f"/api/v1/users/{user_id}")

    assert deleted.status_code == 204
    assert deleted.content == b""
    assert fetched.status_code == 404

