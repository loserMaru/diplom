from typing import Sequence, Any

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Exhibit
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
