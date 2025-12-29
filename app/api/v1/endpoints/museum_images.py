from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.v1.deps import get_db
from app.core.config import settings
from app.crud.base import get_list
from app.models.museum import Museum
from app.models.museum_images import MuseumImage
from app.schemas.museum_images import MuseumImagePublic
from app.services.image_storage import upload_image_to_supabase, delete_image_from_supabase

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

    image_url = await upload_image_to_supabase(
        file=file,
        bucket=settings.supabase_bucket_museums,
        folder=str(museum_id),
    )

    # Создаем запись в базе
    image = MuseumImage(
        museum_id=museum_id,
        image_url=image_url,
        position=position,
    )

    db.add(image)
    await db.commit()
    await db.refresh(image)

    return image


@router.get("/", response_model=list[MuseumImagePublic])
async def get_museum_images(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    return await get_list(
        db=db,
        model=MuseumImage,
        skip=skip,
        limit=limit,
    )


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_museum_image_endpoint(
        image_id: int,
        db: AsyncSession = Depends(get_db),
):
    image = await db.get(MuseumImage, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    # Асинхронное удаление из Supabase
    await delete_image_from_supabase(
        image_url=image.image_url,
        bucket=settings.supabase_bucket_museums
    )

    # Удаляем запись из базы
    await db.delete(image)
    await db.commit()
