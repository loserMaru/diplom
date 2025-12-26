from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.v1.deps import get_db
from app.crud.base import create_with_relations, get_list
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


@router.get("/", response_model=list[ExhibitPublic])
async def get_exhibits(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    return await get_list(
        db=db,
        model=Exhibit,
        skip=skip,
        limit=limit,
        options=[
            selectinload(Exhibit.images),
            selectinload(Exhibit.museum),
        ]
    )
