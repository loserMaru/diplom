import asyncio
import uuid
from urllib.parse import urlparse

from fastapi import UploadFile
from app.core.storage.supabase_connect import supabase
from app.utils.file_storage import validate_image


async def upload_image_to_supabase(
        *,
        file: UploadFile,
        bucket: str,
        folder: str,
) -> str:
    # Валидируем файл и получаем его содержимое в виде bytes
    contents = await validate_image(file)

    # Генерируем уникальное имя
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    path = f"{folder}/{filename}"

    # Загружаем файл в Supabase Storage
    supabase.storage.from_(bucket).upload(
        path,
        contents,
        file_options={
            "content-type": file.content_type,
            "upsert": False
        }
    )

    # Получаем публичный URL (метод возвращает сразу строку)
    public_url = supabase.storage.from_(bucket).get_public_url(path)

    return public_url


async def delete_image_from_supabase(image_url: str, bucket: str):
    """
    Асинхронное удаление изображения из Supabase Storage.
    image_url: публичный URL изображения
    bucket: имя бакета в Supabase
    """
    parsed = urlparse(image_url)
    # путь в хранилище относительно бакета
    path_segments = parsed.path.split(f"/{bucket}/")
    if len(path_segments) != 2:
        raise ValueError(f"Invalid image URL: {image_url}")
    path = path_segments[1]

    # Supabase SDK блокирующий, выполняем в ThreadPoolExecutor
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        None,
        lambda: supabase.storage.from_(bucket).remove([path])
    )

    # Проверяем результат
    if "error" in result and result["error"]:
        raise RuntimeError(f"Failed to delete image from Supabase: {result['error']}")
