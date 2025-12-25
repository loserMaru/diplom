from typing import Type, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, selectinload


async def create_with_relations(
        *,
        db: AsyncSession,
        model: Type[Any],
        data: Any,
        load: InstrumentedAttribute | None = None,
):
    obj = model(**data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)

    if load is None:
        return obj

    stmt = (
        select(model)
        .where(model.id == obj.id)
        .options(selectinload(load))
    )
    result = await db.execute(stmt)
    return result.scalar_one()
