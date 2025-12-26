import uuid
from io import BytesIO
from pathlib import Path

from PIL import Image
from fastapi import UploadFile

from app.core.config import MAX_IMAGE_SIZE, ALLOWED_IMAGE_TYPES, settings
from app.core.exceptions import (
    InvalidImageType,
    ImageTooLarge,
    InvalidImageContent,
)


async def validate_image(file: UploadFile):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise InvalidImageType()

    contents = await file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        raise ImageTooLarge(settings.max_image_size_mb)

    try:
        Image.open(BytesIO(contents)).verify()
    except Exception:
        raise InvalidImageContent()

    return contents


async def save_upload_file(
        *,
        file: UploadFile,
        base_dir: Path,
        sub_dir: str,
        public_prefix: str,
        max_width: int = 1920,
        quality: int = 85,
) -> str:
    contents = await validate_image(file)

    image = Image.open(BytesIO(contents)).convert("RGB")

    if image.width > max_width:
        ratio = max_width / image.width
        new_height = int(image.height * ratio)
        image = image.resize((max_width, new_height))

    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=quality, optimize=True)

    filename = f"{uuid.uuid4()}.jpg"

    target_dir = base_dir / sub_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    file_path = target_dir / filename

    with open(file_path, "wb") as f:
        f.write(buffer.getvalue())

    return f"{public_prefix}/{sub_dir}/{filename}"


def delete_file(path: Path) -> None:
    if path.exists() and path.is_file():
        path.unlink()
