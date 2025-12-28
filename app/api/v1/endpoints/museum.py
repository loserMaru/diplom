from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from app.api.v1.deps import get_db
from app.crud.base import create_with_relations, get_list
from app.models.exhibit import Exhibit
from app.models.museum import Museum
from app.schemas.museum import MuseumCreate, MuseumPublic, MuseumUpdate

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


@router.patch("/{museum_id}", response_model=MuseumPublic)
async def patch_museum(
        museum_id: int,
        museum_in: MuseumUpdate,
        db: AsyncSession = Depends(get_db),
):
    museum = await get_museum(db, museum_id)
    if not museum:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Museum not found.",
        )

    return await update_museum(db, museum, noticing=museum_in)
