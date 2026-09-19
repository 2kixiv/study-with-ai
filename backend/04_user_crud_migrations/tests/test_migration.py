from alembic.runtime.migration import MigrationContext
from sqlalchemy import Boolean, DateTime, String, inspect

from app.database import engine


def test_migration_is_at_head_and_creates_users_table() -> None:
    inspector = inspect(engine)

    assert inspector.has_table("users")
    with engine.connect() as connection:
        assert MigrationContext.configure(connection).get_current_revision() == "0001"


def test_users_table_has_required_schema() -> None:
    inspector = inspect(engine)
    columns = {column["name"]: column for column in inspector.get_columns("users")}
    primary_key = inspector.get_pk_constraint("users")
    unique_constraints = inspector.get_unique_constraints("users")

    assert primary_key["constrained_columns"] == ["id"]
    assert isinstance(columns["email"]["type"], String)
    assert columns["email"]["type"].length == 320
    assert columns["email"]["nullable"] is False
    assert isinstance(columns["name"]["type"], String)
    assert columns["name"]["type"].length == 50
    assert isinstance(columns["is_active"]["type"], Boolean)
    assert columns["is_active"]["nullable"] is False
    assert columns["is_active"]["default"] is not None
    assert isinstance(columns["created_at"]["type"], DateTime)
    assert columns["created_at"]["type"].timezone is True
    assert columns["created_at"]["default"] is not None
    assert columns["updated_at"]["type"].timezone is True
    assert columns["updated_at"]["default"] is not None
    assert any(
        constraint["name"] == "uq_users_email"
        and constraint["column_names"] == ["email"]
        for constraint in unique_constraints
    )
