"""add exhibit models

Revision ID: 94709bd69014
Revises: 
Create Date: 2026-01-08 18:43:01.908389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '94709bd69014'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'exhibit_models',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('model_url', sa.String(length=255), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.Column('exhibit_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['exhibit_id'],
            ['exhibits.id'],
            ondelete='CASCADE'
        ),
        sa.UniqueConstraint('exhibit_id', 'position')
    )


def downgrade() -> None:
    op.drop_table('exhibit_models')
