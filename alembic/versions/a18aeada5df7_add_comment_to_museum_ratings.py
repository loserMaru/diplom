"""add comment to museum_ratings

Revision ID: a18aeada5df7
Revises: 0f6a3e688f5b
Create Date: 2026-02-15 17:46:16.056645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a18aeada5df7'
down_revision: Union[str, Sequence[str], None] = '0f6a3e688f5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Добавляем новое поле comment в museum_ratings
    op.add_column('museum_ratings', sa.Column('comment', sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Убираем поле comment при откате
    op.drop_column('museum_ratings', 'comment')
