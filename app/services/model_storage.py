import uuid

from fastapi import UploadFile
from pathlib import Path

from app.core.config import settings
from app.core.exceptions import InvalidFileType, InvalidMimeType, FileTooLarge
from app.core.storage.supabase_connect import supabase


async def upload_model_to_supabase(
        *,
        file: UploadFile,
        bucket: str,
        folder: str,
) -> str:
    ext = Path(file.filename).suffix.lower()

    if ext not in settings.model_allowed_types:
        raise InvalidFileType()

    if file.content_type not in settings.model_allowed_mime_types:
        raise InvalidMimeType()

    contents = await file.read()
    if len(contents) > settings.max_model_size_mb * 1024 * 1024:
        raise FileTooLarge()

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

    return supabase.storage.from_(bucket).get_public_url(path)


async def delete_model_from_supabase(
        *,
        model_url: str,
        bucket: str,
) -> None:
    path = model_url.split(f"/{bucket}/")[-1]
    supabase.storage.from_(bucket).remove([path])
