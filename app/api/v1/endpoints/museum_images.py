from fastapi import APIRouter, Form, File, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_db
from app.crud.museum_images import create_museum_image
from app.schemas.museum_images import MuseumImagePublic

router = APIRouter()


@router.post("/", response_model=MuseumImagePublic)
async def upload_museum_image(
        museum_id: int = Form(...),
        position: int = Form(...),
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
):
    return await create_museum_image(
        db=db,
        museum_id=museum_id,
        file=file,
        position=position,
    )
