from sqlalchemy.ext.asyncio import AsyncSession

from app.models.exhibit import Exhibit
from app.schemas.exhibit import ExhibitUpdate


async def get_exhibit(
        db: AsyncSession,
        exhibit_id: int
) -> Exhibit | None:
    return await db.get(Exhibit, exhibit_id)


async def update_exhibit(
        db: AsyncSession,
        exhibit: Exhibit,
        data: ExhibitUpdate,
) -> Exhibit:
    if data.name is not None:
        exhibit.name = data.name
    if data.description is not None:
        exhibit.description = data.description

    await db.commit()
    await db.refresh(exhibit)
    return exhibit


async def delete_exhibit(
        db: AsyncSession,
        exhibit: Exhibit
) -> None:
    await db.delete(exhibit)
    await db.commit()