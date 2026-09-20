from sqlalchemy import event
from app.database import engine
from tests.helpers import auth, create_post


def test_list_eager_loads_authors_without_n_plus_one(client) -> None:
    headers = auth(client)
    for index in range(3): create_post(client, headers, f"post {index}")
    statements = []

    def count_query(conn, cursor, statement, parameters, context, executemany):
        if statement.lstrip().upper().startswith("SELECT"): statements.append(statement)

    event.listen(engine, "before_cursor_execute", count_query)
    try:
        response = client.get("/api/v1/posts")
    finally:
        event.remove(engine, "before_cursor_execute", count_query)
    assert response.status_code == 200
    assert len(response.json()["items"]) == 3
    assert len(statements) == 2  # count + 작성자를 포함한 목록

