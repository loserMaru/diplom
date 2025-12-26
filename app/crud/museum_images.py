from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from app.models.museum_images import MuseumImage
from app.utils.file_storage import save_upload_file
from app.crud.image_base import create_image

MUSEUM_IMAGES_ROOT = Path("static/images/museums")


async def create_museum_image(
        *,
        db: AsyncSession,
        museum_id: int,
        file: UploadFile,
        position: int,
) -> MuseumImage:
    image_url = await save_upload_file(
        file=file,
        base_dir=MUSEUM_IMAGES_ROOT,
        sub_dir=str(museum_id),
        public_prefix="/static/images/museums",
    )

    return await create_image(
        db=db,
        model=MuseumImage,
        owner_field="museum_id",
        owner_id=museum_id,
        image_url=image_url,
        position=position,
    )
