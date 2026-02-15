"""add user profile and registered_at

Revision ID: 0f6a3e688f5b
Revises: 389e548f2ac7
Create Date: 2026-02-15 16:03:05.398430

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0f6a3e688f5b'
down_revision: Union[str, Sequence[str], None] = '389e548f2ac7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Добавляем registered_at в users
    op.add_column(
        "users",
        sa.Column(
            "registered_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("TIMEZONE('UTC', now())"),
        ),
    )

    # 2. Создаём таблицу user_profiles
    op.create_table(
        "user_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user_profiles")
    op.drop_column("users", "registered_at")
