from pathlib import Path
from fastapi import UploadFile, HTTPException

from app.core.config import settings


def validate_audio_file(file: UploadFile) -> None:
    suffix = Path(file.filename).suffix.lower()

    allowed_extensions = {
        ext.strip().lower()
        for ext in settings.audio_allowed_types.split(",")
    }

    if suffix not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format: {suffix}",
        )

    allowed_mime_types = {
        mime.strip().lower()
        for mime in settings.audio_allowed_mime_types.split(",")
    }

    if file.content_type not in allowed_mime_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio mime type: {file.content_type}",
        )
