import uuid
from pathlib import Path

from app.models.exhibit_images import ExhibitImage

IMAGES_ROOT = Path("static/images/exhibits")


async def create_exhibit_image(
        *,
        db,
        exhibit_id: int,
        file,
        position: int,
) -> ExhibitImage:
    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"

    exhibit_dir = IMAGES_ROOT / str(exhibit_id)
    exhibit_dir.mkdir(parents=True, exist_ok=True)

    file_path = exhibit_dir / filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    image = ExhibitImage(
        exhibit_id=exhibit_id,
        image_url=f"/static/images/exhibits/{exhibit_id}/{filename}",
        position=position,
    )

    db.add(image)
    await db.commit()
    await db.refresh(image)

    return image
