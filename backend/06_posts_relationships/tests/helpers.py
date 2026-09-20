from fastapi.testclient import TestClient


def auth(client: TestClient, email: str = "user@example.com", name: str = "User") -> dict[str, str]:
    password = "safe-password"
    response = client.post("/api/v1/auth/register", json={"email": email, "name": name, "password": password})
    assert response.status_code == 201
    token = client.post("/api/v1/auth/token", data={"username": email, "password": password}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_post(client: TestClient, headers: dict[str, str], title: str = "FastAPI", content: str = "Relationships"):
    return client.post("/api/v1/posts", headers=headers, json={"title": title, "content": content})

