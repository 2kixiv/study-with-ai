"""create posts

Revision ID: 0002
Revises: 0001
"""
from alembic import op
import sqlalchemy as sa
revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # TODO: 요구사항에 맞는 posts 테이블과 외래 키를 생성하세요.
    raise NotImplementedError


def downgrade() -> None:
    # TODO: posts 테이블을 제거하세요.
    raise NotImplementedError
