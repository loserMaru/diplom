from fastapi import (
    APIRouter,
    Form,
    File,
    UploadFile,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_db, get_current_user
from app.crud.museum_audios import (
    create_museum_audio,
    delete_museum_audio,
)
from app.schemas.museum_audios import MuseumAudioPublic

router = APIRouter(
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=MuseumAudioPublic)
async def upload_museum_audio(
        museum_id: int = Form(...),
        title: str = Form(...),
        position: int = Form(...),
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
):
    return await create_museum_audio(
        db=db,
        museum_id=museum_id,
        title=title,
        position=position,
        file=file,
    )


@router.delete("/{audio_id}", status_code=204)
async def delete_museum_audio_endpoint(
        audio_id: int,
        db: AsyncSession = Depends(get_db),
):
    await delete_museum_audio(
        db=db,
        audio_id=audio_id,
    )
