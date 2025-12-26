from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from app.core.config import settings
from app.models.exhibit_images import ExhibitImage
from app.utils.file_storage import save_upload_file, delete_file
from app.crud.image_base import create_image

EXHIBIT_IMAGES_ROOT = Path("static/images/exhibits")


async def create_exhibit_image(
        *,
        db: AsyncSession,
        exhibit_id: int,
        file: UploadFile,
        position: int,
) -> ExhibitImage:
    image_url = await save_upload_file(
        file=file,
        base_dir=EXHIBIT_IMAGES_ROOT,
        sub_dir=str(exhibit_id),
        public_prefix="/static/images/exhibits",
    )

    return await create_image(
        db=db,
        model=ExhibitImage,
        owner_field="exhibit_id",
        owner_id=exhibit_id,
        image_url=image_url,
        position=position,
    )

async def delete_exhibit_image(
        *,
        db: AsyncSession,
        image_id: int,
) -> None:
    stmt = select(ExhibitImage).where(ExhibitImage.id == image_id)
    result = await db.execute(stmt)
    image = result.scalar_one_or_none()

    if not image:
        raise {"msg": "Image not found"}

    # превращаем URL в путь к файлу
    file_path = Path(settings.base_dir) / image.image_url.lstrip("/")

    delete_file(file_path)

    await db.delete(image)
    await db.commit()