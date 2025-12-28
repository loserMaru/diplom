from sqlalchemy.ext.asyncio import AsyncSession

from app.models.exhibit import Exhibit


async def get_exhibit(
        db: AsyncSession,
        exhibit_id: int
) -> Exhibit | None:
    return await db.get(Exhibit, exhibit_id)
