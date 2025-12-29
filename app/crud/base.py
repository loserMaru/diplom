from typing import Type, Any, TypeVar, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, selectinload


async def create_with_relations(
        *,
        db: AsyncSession,
        model: Type[Any],
        data: Any,
        load: list[InstrumentedAttribute] | None = None,
):
    obj = model(**data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)

    if not load:
        return obj

    stmt = (
        select(model)
        .where(model.id == obj.id)
    )
    for relation in load:
        stmt = stmt.options(selectinload(relation))

    result = await db.execute(stmt)
    return result.scalar_one()


T = TypeVar("T")


async def get_list(
        db: AsyncSession,
        model: Type[T],
        *,
        skip: int = 0,
        limit: int = 100,
        options: Sequence[Any] | None = None,
) -> list[T]:
    stmt = select(model).offset(skip).limit(limit)

    if options:
        stmt = stmt.options(*options)

    result = await db.execute(stmt)
    return list(result.scalars().all())
