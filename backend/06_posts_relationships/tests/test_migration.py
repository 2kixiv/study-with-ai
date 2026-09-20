from sqlalchemy import inspect
from app.database import engine


def test_posts_schema_and_cascade_foreign_key() -> None:
    inspector = inspect(engine)
    columns = {column["name"]: column for column in inspector.get_columns("posts")}
    foreign_keys = inspector.get_foreign_keys("posts")
    assert columns["title"]["type"].length == 200
    assert columns["title"]["nullable"] is False
    assert columns["content"]["nullable"] is False
    assert columns["author_id"]["nullable"] is False
    assert columns["created_at"]["default"] is not None
    assert columns["updated_at"]["default"] is not None
    assert len(foreign_keys) == 1
    assert foreign_keys[0]["referred_table"] == "users"
    assert foreign_keys[0]["referred_columns"] == ["id"]
    assert foreign_keys[0]["options"].get("ondelete") == "CASCADE"

