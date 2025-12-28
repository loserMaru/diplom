from sqlalchemy.ext.asyncio import AsyncSession

from app.models.museum import Museum


async def get_museum(db: AsyncSession, museum_id: int) -> Museum | None:
    return await db.get(Museum, museum_id)
