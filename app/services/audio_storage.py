import uuid
from pathlib import Path
from fastapi import UploadFile

from app.core.config import settings
from app.core.storage.supabase_connect import supabase
from app.core.exceptions import (
    InvalidFileType,
    InvalidMimeType,
    FileTooLarge,
)
from app.services.audio_utils import get_audio_duration_seconds


async def upload_audio_to_supabase(
        *,
        file: UploadFile,
        bucket: str,
        folder: str,
) -> tuple[str, int]:
    ext = Path(file.filename).suffix.lower()

    if ext not in settings.audio_allowed_types:
        raise InvalidFileType()

    if file.content_type not in settings.audio_allowed_mime_types:
        raise InvalidMimeType()

    contents = await file.read()

    if len(contents) > settings.max_audio_size_mb * 1024 * 1024:
        raise FileTooLarge()

    duration = get_audio_duration_seconds(contents)

    filename = f"{uuid.uuid4()}{ext}"
    path = f"{folder}/{filename}"

    supabase.storage.from_(bucket).upload(
        path,
        contents,
        file_options={
            "content-type": file.content_type,
            "upsert": False,
        },
    )

    url = supabase.storage.from_(bucket).get_public_url(path)
    return url, duration


async def delete_audio_from_supabase(
        *,
        audio_url: str,
        bucket: str,
) -> None:
    path = audio_url.split(f"/{bucket}/")[-1]
    supabase.storage.from_(bucket).remove([path])
