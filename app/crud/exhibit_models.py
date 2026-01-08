from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, HTTPException

from app.core.config import settings
from app.models.exhibit import Exhibit
from app.models.exhibit_models import ExhibitModel
from app.services.model_storage import (
    upload_model_to_supabase,
    delete_model_from_supabase,
)
from app.utils.model_validation import validate_3d_model_file


async def create_exhibit_model(
        *,
        db: AsyncSession,
        exhibit_id: int,
        file: UploadFile,
        position: int,
) -> ExhibitModel:
    exhibit = await db.scalar(
        select(Exhibit).where(Exhibit.id == exhibit_id)
    )
    if not exhibit:
        raise HTTPException(status_code=404, detail="Exhibit not found")

    validate_3d_model_file(file)

    model_url = await upload_model_to_supabase(
        file=file,
        bucket=settings.supabase_bucket_exhibit_models,
        folder=str(exhibit_id),
    )

    model = ExhibitModel(
        exhibit_id=exhibit_id,
        model_url=model_url,
        position=position,
    )

    db.add(model)
    await db.commit()
    await db.refresh(model)

    return model


async def delete_exhibit_model(
        *,
        db: AsyncSession,
        model_id: int,
) -> None:
    model = await db.get(ExhibitModel, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    await delete_model_from_supabase(
        model_url=model.model_url,
        bucket=settings.supabase_bucket_exhibit_models,
    )

    await db.delete(model)
    await db.commit()
