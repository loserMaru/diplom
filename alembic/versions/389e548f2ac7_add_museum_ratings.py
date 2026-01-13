"""add museum ratings

Revision ID: 389e548f2ac7
Revises: d73056d73c4b
Create Date: 2026-01-12 22:15:00.434723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '389e548f2ac7'
down_revision: Union[str, Sequence[str], None] = 'd73056d73c4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "museum_ratings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("museum_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["museum_id"], ["museums.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "museum_id"),
        sa.CheckConstraint("rating BETWEEN 1 AND 5"),
    )

    op.add_column(
        "museums",
        sa.Column("rating_avg", sa.Float(), server_default="0", nullable=False),
    )
    op.add_column(
        "museums",
        sa.Column("rating_count", sa.Integer(), server_default="0", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("museums", "rating_count")
    op.drop_column("museums", "rating_avg")
    op.drop_table("museum_ratings")
