from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.museum import Museum
from app.models.museum_ratings import MuseumRating
from app.models.user_profile import UserProfile
from app.schemas.museum_ratings import MuseumRatingPublic


async def rate_museum(
        *,
        db: AsyncSession,
        user_id: int,
        museum_id: int,
        rating: int,
        comment: str | None = None
) -> None:
    if not 1 <= rating <= 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    museum = await db.get(Museum, museum_id)
    if not museum:
        raise HTTPException(status_code=404, detail="Museum not found")

    # Проверяем, есть ли уже рейтинг пользователя для музея
    existing = await db.scalar(
        select(MuseumRating).where(
            MuseumRating.user_id == user_id,
            MuseumRating.museum_id == museum_id,
        )
    )

    if existing:
        old_rating = existing.rating
        existing.rating = rating
        existing.comment = comment
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
                comment=comment,
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
) -> list[MuseumRatingPublic]:
    stmt = (
        select(
            MuseumRating,
            UserProfile.first_name,
            UserProfile.last_name
        )
        .join(UserProfile, UserProfile.user_id == MuseumRating.user_id)
        .where(MuseumRating.user_id == user_id)
        .order_by(MuseumRating.id.desc())
    )

    result = await db.execute(stmt)
    ratings = []

    for rating, first_name, last_name in result.all():
        ratings.append(
            MuseumRatingPublic(
                id=rating.id,
                rating=rating.rating,
                museum_id=rating.museum_id,
                comment=rating.comment,
                first_name=first_name,
                last_name=last_name
            )
        )

    return ratings


async def delete_museum_rating(
        *,
        db: AsyncSession,
        user_id: int,
        museum_id: int,
) -> None:
    museum = await db.get(Museum, museum_id)
    if not museum:
        raise HTTPException(status_code=404, detail="Museum not found")

    rating = await db.scalar(
        select(MuseumRating).where(
            MuseumRating.user_id == user_id,
            MuseumRating.museum_id == museum_id,
        )
    )
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    if museum.rating_count <= 1:
        museum.rating_count = 0
        museum.rating_avg = 0
    else:
        museum.rating_avg = (
            (museum.rating_avg * museum.rating_count - rating.rating)
            / (museum.rating_count - 1)
        )
        museum.rating_count -= 1

    await db.delete(rating)
    await db.commit()