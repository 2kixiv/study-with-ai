from fastapi.testclient import TestClient


def create_note(
    client: TestClient,
    title: str = "SQLAlchemy",
    content: str = "Learn database sessions",
):
    return client.post(
        "/api/v1/notes",
        json={"title": title, "content": content},
    )


def test_health_checks_database(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_create_note_uses_database_generated_values(client: TestClient) -> None:
    response = create_note(client, title="  PostgreSQL  ")

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "PostgreSQL"
    assert body["content"] == "Learn database sessions"
    assert body["created_at"] is not None


def test_create_note_validates_input(client: TestClient) -> None:
    invalid_payloads = [
        {"title": "   ", "content": "valid"},
        {"title": "a" * 101, "content": "valid"},
        {"title": "valid", "content": "   "},
        {"title": "valid", "content": "a" * 5001},
        {"title": "valid", "content": "valid", "unknown": True},
    ]

    for payload in invalid_payloads:
        response = client.post("/api/v1/notes", json=payload)
        assert response.status_code == 422, payload


def test_list_notes_returns_id_order(client: TestClient) -> None:
    assert client.get("/api/v1/notes").json() == []

    create_note(client, title="first")
    create_note(client, title="second")

    response = client.get("/api/v1/notes")

    assert response.status_code == 200
    assert [note["title"] for note in response.json()] == ["first", "second"]
    assert [note["id"] for note in response.json()] == [1, 2]


def test_get_note_and_missing_note(client: TestClient) -> None:
    created = create_note(client).json()

    found = client.get(f"/api/v1/notes/{created['id']}")
    missing = client.get("/api/v1/notes/999")

    assert found.status_code == 200
    assert found.json() == created
    assert missing.status_code == 404
    assert missing.json() == {"detail": "Study note not found"}


def test_delete_note_removes_database_row(client: TestClient) -> None:
    note_id = create_note(client).json()["id"]

    deleted = client.delete(f"/api/v1/notes/{note_id}")
    fetched = client.get(f"/api/v1/notes/{note_id}")

    assert deleted.status_code == 204
    assert deleted.content == b""
    assert fetched.status_code == 404


def test_delete_missing_note_returns_404(client: TestClient) -> None:
    response = client.delete("/api/v1/notes/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Study note not found"}

