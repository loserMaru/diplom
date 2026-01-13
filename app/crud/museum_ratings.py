from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.museum import Museum
from app.models.museum_ratings import MuseumRating


async def rate_museum(
        *,
        db: AsyncSession,
        user_id: int,
        museum_id: int,
        rating: int,
) -> None:
    if not 1 <= rating <= 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    museum = await db.get(Museum, museum_id)
    if not museum:
        raise HTTPException(status_code=404, detail="Museum not found")

    existing = await db.scalar(
        select(MuseumRating).where(
            MuseumRating.user_id == user_id,
            MuseumRating.museum_id == museum_id,
        )
    )

    if existing:
        old_rating = existing.rating
        existing.rating = rating
        delta = rating - old_rating
        museum.rating_avg = (
                (museum.rating_avg * museum.rating_count + delta)
                / museum.rating_count
        )
    else:
        db.add(
            MuseumRating(
                user_id=user_id,
                museum_id=museum_id,
                rating=rating,
            )
        )
        museum.rating_count += 1
        museum.rating_avg = (
                (museum.rating_avg * (museum.rating_count - 1) + rating)
                / museum.rating_count
        )

    await db.commit()


async def get_my_museum_ratings(
        *,
        db: AsyncSession,
        user_id: int,
) -> list[MuseumRating]:
    stmt = (
        select(MuseumRating)
        .where(MuseumRating.user_id == user_id)
        .order_by(MuseumRating.id.desc())
    )

    result = await db.execute(stmt)
    return list(result.scalars().all())
