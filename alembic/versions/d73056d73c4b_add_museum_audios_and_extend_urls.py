"""add museum audios and extend urls

Revision ID: d73056d73c4b
Revises: 138797f366f3
Create Date: 2026-01-10 17:23:55.590732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd73056d73c4b'
down_revision: Union[str, Sequence[str], None] = '138797f366f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Увеличиваем длину URL в существующих таблицах
    op.alter_column(
        "museum_images",
        "image_url",
        type_=sa.String(length=512),
        existing_type=sa.String(length=255),
        nullable=False,
    )

    op.alter_column(
        "exhibit_images",
        "image_url",
        type_=sa.String(length=512),
        existing_type=sa.String(length=255),
        nullable=False,
    )

    op.alter_column(
        "exhibit_models",
        "model_url",
        type_=sa.String(length=512),
        existing_type=sa.String(length=255),
        nullable=False,
    )

    # 2. Создаём таблицу museum_audios
    op.create_table(
        "museum_audios",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("audio_url", sa.String(length=512), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("duration", sa.Integer(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("museum_id", sa.Integer(), nullable=False),

        sa.ForeignKeyConstraint(
            ["museum_id"],
            ["museums.id"],
            ondelete="CASCADE",
        ),

        sa.UniqueConstraint(
            "museum_id",
            "position",
            name="uq_museum_audio_position",
        ),
    )


def downgrade():
    # Откат: удаляем таблицу
    op.drop_table("museum_audios")

    # Возвращаем длину URL обратно (если потребуется)
    op.alter_column(
        "exhibit_models",
        "model_url",
        type_=sa.String(length=255),
        existing_type=sa.String(length=512),
        nullable=False,
    )

    op.alter_column(
        "exhibit_images",
        "image_url",
        type_=sa.String(length=255),
        existing_type=sa.String(length=512),
        nullable=False,
    )

    op.alter_column(
        "museum_images",
        "image_url",
        type_=sa.String(length=255),
        existing_type=sa.String(length=512),
        nullable=False,
    )