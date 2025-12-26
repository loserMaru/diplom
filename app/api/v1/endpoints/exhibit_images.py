from fastapi import APIRouter, Form, File, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.v1.deps import get_db
from app.crud.exhibit_images import create_exhibit_image, delete_exhibit_image
from app.schemas.exhibit_image import ExhibitImagePublic

router = APIRouter()


@router.post("/", response_model=ExhibitImagePublic)
async def upload_exhibit_image(
        exhibit_id: int = Form(...),
        position: int = Form(...),
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
):
    return await create_exhibit_image(
        db=db,
        exhibit_id=exhibit_id,
        file=file,
        position=position,
    )


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exhibit_image_endpoint(
        image_id: int,
        db: AsyncSession = Depends(get_db),
):
    await delete_exhibit_image(db=db, image_id=image_id)