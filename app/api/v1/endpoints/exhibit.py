from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_db
from app.crud.base import create_with_relations
from app.models.exhibit import Exhibit
from app.schemas.exhibit import ExhibitPublic, ExhibitCreate

router = APIRouter()


@router.post("/", response_model=ExhibitPublic)
async def create_exhibit(
        data: ExhibitCreate,
        db: AsyncSession = Depends(get_db),
):
    return await create_with_relations(
        db=db,
        model=Exhibit,
        data=data,
        load=Exhibit.images
    )
