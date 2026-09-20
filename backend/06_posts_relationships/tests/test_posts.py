from fastapi.testclient import TestClient
from tests.helpers import auth, create_post


def test_create_uses_authenticated_author_and_validates(client: TestClient) -> None:
    headers = auth(client, name="Kim")
    response = create_post(client, headers, "  FastAPI  ", "  content  ")
    assert response.status_code == 201
    assert response.json()["title"] == "FastAPI"
    assert response.json()["author"] == {"id": 1, "name": "Kim"}
    assert "email" not in response.json()["author"]
    assert client.post("/api/v1/posts", json={"title": "x", "content": "y"}).status_code == 401
    assert create_post(client, headers, title=" ").status_code == 422


def test_list_searches_paginates_and_returns_metadata(client: TestClient) -> None:
    headers = auth(client)
    create_post(client, headers, "FastAPI intro", "one")
    create_post(client, headers, "PostgreSQL", "fastapi with database")
    create_post(client, headers, "Unrelated", "other")
    response = client.get("/api/v1/posts?q=FASTAPI&page=1&size=1")
    body = response.json()
    assert response.status_code == 200
    assert body["total"] == 2
    assert body["pages"] == 2
    assert body["page"] == 1 and body["size"] == 1
    assert [item["title"] for item in body["items"]] == ["PostgreSQL"]


def test_empty_page_has_zero_pages(client: TestClient) -> None:
    body = client.get("/api/v1/posts?q=missing").json()
    assert body == {"items": [], "total": 0, "page": 1, "size": 20, "pages": 0}


def test_get_post_and_missing_post_are_public(client: TestClient) -> None:
    created = create_post(client, auth(client)).json()
    assert client.get(f"/api/v1/posts/{created['id']}").json() == created
    missing = client.get("/api/v1/posts/999")
    assert missing.status_code == 404
    assert missing.json() == {"detail": "Post not found"}


def test_owner_can_partially_update(client: TestClient) -> None:
    headers = auth(client)
    created = create_post(client, headers, content="original").json()
    response = client.patch(f"/api/v1/posts/{created['id']}", headers=headers, json={"title": "Updated"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"
    assert response.json()["content"] == "original"
    assert client.patch(f"/api/v1/posts/{created['id']}", headers=headers, json={}).status_code == 422


def test_non_owner_cannot_update_or_delete(client: TestClient) -> None:
    owner = auth(client, "owner@example.com", "Owner")
    post_id = create_post(client, owner).json()["id"]
    stranger = auth(client, "stranger@example.com", "Stranger")
    updated = client.patch(f"/api/v1/posts/{post_id}", headers=stranger, json={"title": "Stolen"})
    deleted = client.delete(f"/api/v1/posts/{post_id}", headers=stranger)
    assert updated.status_code == 403 and updated.json() == {"detail": "Not post owner"}
    assert deleted.status_code == 403 and deleted.json() == {"detail": "Not post owner"}


def test_owner_can_delete(client: TestClient) -> None:
    headers = auth(client)
    post_id = create_post(client, headers).json()["id"]
    response = client.delete(f"/api/v1/posts/{post_id}", headers=headers)
    assert response.status_code == 204 and response.content == b""
    assert client.get(f"/api/v1/posts/{post_id}").status_code == 404

