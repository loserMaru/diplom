from typing import Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


async def create_image(
        *,
        db: AsyncSession,
        model: Type[T],
        owner_field: str,
        owner_id: int,
        image_url: str,
        position: int,
) -> T:
    image = model(
        **{
            owner_field: owner_id,
            "image_url": image_url,
            "position": position,
        }
    )

    db.add(image)
    await db.commit()
    await db.refresh(image)

    return image
