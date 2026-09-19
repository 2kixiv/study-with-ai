from fastapi.testclient import TestClient


def create_record(
    client: TestClient, topic: str = "FastAPI", minutes: int = 30
):
    return client.post(
        "/api/v1/study-records",
        json={"topic": topic, "minutes": minutes},
    )


def test_create_record_returns_201_and_generated_fields(client: TestClient) -> None:
    response = create_record(client)

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "topic": "FastAPI",
        "minutes": 30,
        "completed": False,
    }


def test_create_record_trims_topic(client: TestClient) -> None:
    response = create_record(client, topic="  HTTP status code  ")

    assert response.status_code == 201
    assert response.json()["topic"] == "HTTP status code"


def test_create_record_rejects_invalid_topic(client: TestClient) -> None:
    empty = create_record(client, topic="   ")
    too_long = create_record(client, topic="a" * 101)

    assert empty.status_code == 422
    assert too_long.status_code == 422


def test_create_record_rejects_invalid_minutes(client: TestClient) -> None:
    zero = create_record(client, minutes=0)
    too_large = create_record(client, minutes=721)

    assert zero.status_code == 422
    assert too_large.status_code == 422


def test_list_records_returns_creation_order(client: TestClient) -> None:
    assert client.get("/api/v1/study-records").json() == []

    create_record(client, topic="first", minutes=10)
    create_record(client, topic="second", minutes=20)
    response = client.get("/api/v1/study-records")

    assert response.status_code == 200
    assert [item["topic"] for item in response.json()] == ["first", "second"]
    assert [item["id"] for item in response.json()] == [1, 2]


def test_get_existing_record(client: TestClient) -> None:
    created = create_record(client).json()

    response = client.get(f"/api/v1/study-records/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_missing_record_returns_404(client: TestClient) -> None:
    response = client.get("/api/v1/study-records/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Study record not found"}


def test_complete_record_is_idempotent(client: TestClient) -> None:
    record_id = create_record(client).json()["id"]

    first = client.patch(f"/api/v1/study-records/{record_id}/complete")
    second = client.patch(f"/api/v1/study-records/{record_id}/complete")

    assert first.status_code == 200
    assert first.json()["completed"] is True
    assert second.status_code == 200
    assert second.json() == first.json()


def test_complete_missing_record_returns_404(client: TestClient) -> None:
    response = client.patch("/api/v1/study-records/999/complete")

    assert response.status_code == 404
    assert response.json() == {"detail": "Study record not found"}
