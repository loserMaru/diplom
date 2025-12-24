import uuid
from pathlib import Path

from app.models.museum_images import MuseumImage

IMAGES_ROOT = Path("static/images/museums")


async def create_museum_image(
        *,
        db,
        museum_id: int,
        file,
        position: int,
) -> MuseumImage:
    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"

    museum_dir = IMAGES_ROOT / str(museum_id)
    museum_dir.mkdir(parents=True, exist_ok=True)

    file_path = museum_dir / filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    image = MuseumImage(
        museum_id=museum_id,
        image_url=f"/static/images/museums/{museum_id}/{filename}",
        position=position,
    )

    db.add(image)
    await db.commit()
    await db.refresh(image)

    return image
