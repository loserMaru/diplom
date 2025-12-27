from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.v1.deps import get_db
from app.crud.exhibit_images import create_exhibit_image, delete_exhibit_image
from app.models.exhibit import Exhibit
from app.models.exhibit_images import ExhibitImage
from app.schemas.exhibit_image import ExhibitImagePublic

router = APIRouter()


@router.post("/", response_model=ExhibitImagePublic)
async def upload_exhibit_image(
        exhibit_id: int = Form(...),
        position: int = Form(...),
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
):
    exhibit = await db.scalar(
        select(Exhibit).where(Exhibit.id == exhibit_id)
    )
    if not exhibit:
        raise HTTPException(
            status_code=404,
            detail="Exhibit not found"
        )

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
    image = await db.get(ExhibitImage, image_id)
    if not image:
        raise HTTPException(
            status_code=404,
            detail="Image not found"
        )

    await delete_exhibit_image(db=db, image_id=image_id)
