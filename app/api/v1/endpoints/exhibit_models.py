from fastapi import (
    APIRouter,
    Form,
    File,
    UploadFile,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_db, get_current_user
from app.crud.exhibit_models import (
    create_exhibit_model,
    delete_exhibit_model,
)
from app.schemas.exhibit_models import ExhibitModelPublic

router = APIRouter(
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=ExhibitModelPublic)
async def upload_exhibit_model(
        exhibit_id: int = Form(...),
        position: int = Form(...),
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
):
    return await create_exhibit_model(
        db=db,
        exhibit_id=exhibit_id,
        file=file,
        position=position,
    )


@router.delete("/{model_id}", status_code=204)
async def delete_exhibit_model_endpoint(
        model_id: int,
        db: AsyncSession = Depends(get_db),
):
    await delete_exhibit_model(
        db=db,
        model_id=model_id,
    )
