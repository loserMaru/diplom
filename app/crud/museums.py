from sqlalchemy.ext.asyncio import AsyncSession

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


async def delete_museum(db: AsyncSession, museum: Museum) -> None:
    await db.delete(museum)
    await db.commit()
