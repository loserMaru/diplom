from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from app.models.exhibit_images import ExhibitImage
from app.utils.file_storage import save_upload_file
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
