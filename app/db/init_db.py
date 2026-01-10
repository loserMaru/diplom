from app.db.base import Base  # type: ignore
from app.models import (
    user,
    museum,
    museum_audios,
    museum_images,
    exhibit,
    exhibit_images,
    exhibit_models,
)


def init_models() -> None:
    _ = (
        user,
        museum,
        museum_audios,
        museum_images,
        exhibit,
        exhibit_images,
        exhibit_models,
    )
