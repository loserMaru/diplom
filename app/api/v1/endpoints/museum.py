from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.v1.deps import get_db
from app.crud.base import create_with_relations, get_list
from app.models.exhibit import Exhibit
from app.models.museum import Museum
from app.schemas.museum import MuseumCreate, MuseumPublic

router = APIRouter()


@router.post("/", response_model=MuseumPublic)
async def create_museum(
        data: MuseumCreate,
        db: AsyncSession = Depends(get_db),
):
    return await create_with_relations(
        db=db,
        model=Museum,
        data=data,
        load=Museum.images,
    )


@router.get("/", response_model=list[MuseumPublic])
async def get_museums(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    return await get_list(
        db=db,
        model=Museum,
        skip=skip,
        limit=limit,
        options=[
            selectinload(Museum.images),
            selectinload(Museum.exhibits).selectinload(Exhibit.images)
        ],
    )
