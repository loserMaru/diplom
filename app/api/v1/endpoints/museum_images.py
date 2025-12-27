from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.v1.deps import get_db
from app.crud.museum_images import create_museum_image, delete_museum_image
from app.models.museum import Museum
from app.models.museum_images import MuseumImage
from app.schemas.museum_images import MuseumImagePublic

router = APIRouter()


@router.post("/", response_model=MuseumImagePublic)
async def upload_museum_image(
        museum_id: int = Form(...),
        position: int = Form(...),
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
):
    museum = await db.scalar(
        select(Museum).where(Museum.id == museum_id)
    )
    if not museum:
        raise HTTPException(
            status_code=404,
            detail="Museum not found"
        )

    return await create_museum_image(
        db=db,
        museum_id=museum_id,
        file=file,
        position=position,
    )


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_museum_image_endpoint(
        image_id: int,
        db: AsyncSession = Depends(get_db),
):
    image = await db.get(MuseumImage, image_id)
    if not image:
        raise HTTPException(
            status_code=404,
            detail="Image not found"
        )

    await delete_museum_image(db=db, image_id=image_id)
