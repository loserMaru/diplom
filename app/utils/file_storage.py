import uuid
from pathlib import Path

from fastapi import UploadFile


async def save_upload_file(
        *,
        file: UploadFile,
        base_dir: Path,
        sub_dir: str,
        public_prefix: str,
) -> str:
    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"

    target_dir = base_dir / sub_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    file_path = target_dir / filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return f"{public_prefix}/{sub_dir}/{filename}"
