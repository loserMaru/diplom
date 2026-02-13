from typing import Sequence, Any

from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Exhibit, MuseumRating
from app.models.museum import Museum
from app.schemas.museum import MuseumUpdate


async def get_museum(db: AsyncSession, museum_id: int) -> Museum | None:
    return await db.get(Museum, museum_id)


async def update_museum(
        db: AsyncSession,
        museum: Museum,
        data: MuseumUpdate,
) -> Museum:
    if data.name is not None:
        museum.name = data.name
    if data.description is not None:
        museum.description = data.description

    await db.commit()
    await db.refresh(museum)
    return museum


async def search_museums(
        *,
        db: AsyncSession,
        query: str,
        skip: int = 0,
        limit: int = 100,
        options: Sequence[Any] | None = None,
) -> list[Museum]:
    stmt = (
        select(Museum)
        .outerjoin(Exhibit, Exhibit.museum_id == Museum.id)
        .where(
            or_(
                Museum.name.ilike(f"%{query}%"),
                Exhibit.name.ilike(f"%{query}%"),
            )
        )
        .distinct()
        .offset(skip)
        .limit(limit)
    )

    if options:
        stmt = stmt.options(*options)

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def delete_museum(db: AsyncSession, museum: Museum) -> None:
    await db.delete(museum)
    await db.commit()


async def get_museum_rating_stats(
        db: AsyncSession,
        museum_id: int,
) -> dict:
    stmt = (
        select(
            MuseumRating.rating,
            func.count(MuseumRating.id).label("count")
        )
        .where(MuseumRating.museum_id == museum_id)
        .group_by(MuseumRating.rating)
    )

    result = await db.execute(stmt)
    rows = result.all()

    distribution = {i: 0 for i in range(1, 6)}
    total_count = 0
    rating_sum = 0

    for rating, count in rows:
        distribution[rating] = count
        total_count += count
        rating_sum += rating * count

    avg = rating_sum / total_count if total_count else 0.0

    return {
        "rating_count": total_count,
        "rating_avg": avg,
        "rating_distribution": distribution
    }


async def get_museums_rating_stats_bulk(
        db: AsyncSession,
        museum_ids: list[int],
) -> dict[int, dict]:
    if not museum_ids:
        return {}

    stmt = (
        select(
            MuseumRating.museum_id,
            MuseumRating.rating,
            func.count(MuseumRating.id).label("count")
        )
        .where(MuseumRating.museum_id.in_(museum_ids))
        .group_by(MuseumRating.museum_id, MuseumRating.rating)
    )

    result = await db.execute(stmt)
    rows = result.all()

    stats = {
        museum_id: {
            "rating_count": 0,
            "rating_sum": 0,
            "rating_distribution": {i: 0 for i in range(1, 6)}
        }
        for museum_id in museum_ids
    }

    for museum_id, rating, count in rows:
        stats[museum_id]["rating_distribution"][rating] = count
        stats[museum_id]["rating_count"] += count
        stats[museum_id]["rating_sum"] += rating * count

    for museum_id in stats:
        count = stats[museum_id]["rating_count"]
        stats[museum_id]["rating_avg"] = (
            stats[museum_id]["rating_sum"] / count if count else 0
        )
        del stats[museum_id]["rating_sum"]

    return stats
