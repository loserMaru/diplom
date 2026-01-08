from pathlib import Path
from fastapi import UploadFile, HTTPException

from app.core.config import settings


def validate_3d_model_file(file: UploadFile) -> None:
    suffix = Path(file.filename).suffix.lower()

    allowed_extensions = {
        ext.strip().lower()
        for ext in settings.model_allowed_types.split(",")
    }

    if suffix not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported model format: {suffix}",
        )
