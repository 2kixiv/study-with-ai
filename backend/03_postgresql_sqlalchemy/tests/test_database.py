from sqlalchemy import Text, inspect, select

from app.database import SessionLocal, engine
from app.models import StudyNote


def test_uses_postgresql() -> None:
    assert engine.dialect.name == "postgresql"


def test_model_has_required_database_columns(client) -> None:
    columns = {column.name: column for column in inspect(StudyNote).columns}

    assert columns["id"].primary_key is True
    assert columns["title"].type.length == 100
    assert columns["title"].nullable is False
    assert isinstance(columns["content"].type, Text)
    assert columns["content"].nullable is False
    assert columns["created_at"].type.timezone is True
    assert columns["created_at"].nullable is False
    assert columns["created_at"].server_default is not None


def test_created_note_is_visible_in_a_new_session(client) -> None:
    response = client.post(
        "/api/v1/notes",
        json={"title": "Persistence", "content": "Stored in PostgreSQL"},
    )
    note_id = response.json()["id"]

    with SessionLocal() as new_session:
        stored = new_session.scalar(
            select(StudyNote).where(StudyNote.id == note_id)
        )

    assert stored is not None
    assert stored.title == "Persistence"

