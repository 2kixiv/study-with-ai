from fastapi.testclient import TestClient


def create_task(
    client: TestClient,
    title: str = "Dependency Injection",
    priority: str | None = None,
):
    payload = {"title": title}
    if priority is not None:
        payload["priority"] = priority
    return client.post("/api/v1/study-tasks", json=payload)


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task_uses_defaults_and_trims_title(client: TestClient) -> None:
    response = create_task(client, title="  Service layer  ")

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Service layer",
        "priority": "medium",
        "completed": False,
    }


def test_create_task_accepts_priority(client: TestClient) -> None:
    response = create_task(client, priority="high")

    assert response.status_code == 201
    assert response.json()["priority"] == "high"


def test_create_task_validates_input(client: TestClient) -> None:
    invalid_payloads = [
        {"title": "   "},
        {"title": "a" * 101},
        {"title": "valid", "priority": "urgent"},
        {"title": "valid", "unknown": True},
    ]

    for payload in invalid_payloads:
        response = client.post("/api/v1/study-tasks", json=payload)
        assert response.status_code == 422, payload


def test_list_tasks_can_filter_by_completed(client: TestClient) -> None:
    first_id = create_task(client, "first").json()["id"]
    create_task(client, "second")
    client.patch(f"/api/v1/study-tasks/{first_id}/complete")

    all_tasks = client.get("/api/v1/study-tasks")
    completed = client.get("/api/v1/study-tasks?completed=true")
    active = client.get("/api/v1/study-tasks?completed=false")

    assert [task["title"] for task in all_tasks.json()] == ["first", "second"]
    assert [task["title"] for task in completed.json()] == ["first"]
    assert [task["title"] for task in active.json()] == ["second"]


def test_get_task_and_missing_task(client: TestClient) -> None:
    created = create_task(client).json()

    found = client.get(f"/api/v1/study-tasks/{created['id']}")
    missing = client.get("/api/v1/study-tasks/999")

    assert found.status_code == 200
    assert found.json() == created
    assert missing.status_code == 404
    assert missing.json() == {"detail": "Study task not found"}


def test_active_titles_are_unique_ignoring_case(client: TestClient) -> None:
    assert create_task(client, "FastAPI").status_code == 201

    duplicate = create_task(client, "  fastapi  ")

    assert duplicate.status_code == 409
    assert duplicate.json() == {
        "detail": "Active task with this title already exists"
    }


def test_completed_title_can_be_created_again(client: TestClient) -> None:
    task_id = create_task(client, "FastAPI").json()["id"]
    client.patch(f"/api/v1/study-tasks/{task_id}/complete")

    response = create_task(client, "fastapi")

    assert response.status_code == 201
    assert response.json()["id"] == 2


def test_completing_twice_returns_conflict(client: TestClient) -> None:
    task_id = create_task(client).json()["id"]

    first = client.patch(f"/api/v1/study-tasks/{task_id}/complete")
    second = client.patch(f"/api/v1/study-tasks/{task_id}/complete")

    assert first.status_code == 200
    assert first.json()["completed"] is True
    assert second.status_code == 409
    assert second.json() == {"detail": "Study task is already completed"}


def test_complete_missing_task_returns_404(client: TestClient) -> None:
    response = client.patch("/api/v1/study-tasks/999/complete")

    assert response.status_code == 404
    assert response.json() == {"detail": "Study task not found"}


def test_delete_task_returns_empty_204_and_removes_it(client: TestClient) -> None:
    task_id = create_task(client).json()["id"]

    deleted = client.delete(f"/api/v1/study-tasks/{task_id}")
    fetched = client.get(f"/api/v1/study-tasks/{task_id}")

    assert deleted.status_code == 204
    assert deleted.content == b""
    assert fetched.status_code == 404


def test_delete_missing_task_returns_404(client: TestClient) -> None:
    response = client.delete("/api/v1/study-tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Study task not found"}

