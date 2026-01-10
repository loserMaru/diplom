from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, HTTPException

from app.core.config import settings
from app.models.museum import Museum
from app.models.museum_audios import MuseumAudio
from app.services.audio_storage import (
    upload_audio_to_supabase,
    delete_audio_from_supabase,
)
from app.utils.audio_validation import validate_audio_file


async def create_museum_audio(
        *,
        db: AsyncSession,
        museum_id: int,
        title: str,
        position: int,
        file: UploadFile,
) -> MuseumAudio:
    museum = await db.scalar(
        select(Museum).where(Museum.id == museum_id)
    )
    if not museum:
        raise HTTPException(status_code=404, detail="Museum not found")

    validate_audio_file(file)

    audio_url, duration = await upload_audio_to_supabase(
        file=file,
        bucket=settings.supabase_bucket_museum_audios,
        folder=str(museum_id),
    )

    audio = MuseumAudio(
        museum_id=museum_id,
        title=title,
        audio_url=audio_url,
        duration=duration,
        position=position,
    )

    db.add(audio)
    await db.commit()
    await db.refresh(audio)

    return audio


async def delete_museum_audio(
        *,
        db: AsyncSession,
        audio_id: int,
) -> None:
    audio = await db.get(MuseumAudio, audio_id)
    if not audio:
        raise HTTPException(status_code=404, detail="Audio not found")

    await delete_audio_from_supabase(
        audio_url=audio.audio_url,
        bucket=settings.supabase_bucket_museum_audios,
    )

    await db.delete(audio)
    await db.commit()
