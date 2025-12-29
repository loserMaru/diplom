from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from app.api.v1.deps import get_db
from app.crud.base import create_with_relations, get_list
from app.crud.exhibits import get_exhibit, update_exhibit, delete_exhibit
from app.models.exhibit import Exhibit
from app.schemas.exhibit import ExhibitPublic, ExhibitCreate, ExhibitUpdate

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
        load=[Exhibit.images, Exhibit.museum],
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


@router.patch("/{exhibit_id}", response_model=ExhibitPublic)
async def patch_exhibit(
        exhibit_id: int,
        data: ExhibitUpdate,
        db: AsyncSession = Depends(get_db),
):
    exhibit = await get_exhibit(db, exhibit_id)
    if not exhibit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exhibit not found",
        )

    return await update_exhibit(db, exhibit, data)


@router.delete("/{exhibit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_exhibit(
        exhibit_id: int,
        db: AsyncSession = Depends(get_db),
):
    exhibit = await get_exhibit(db, exhibit_id)
    if not exhibit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exhibit not found",
        )

    await delete_exhibit(db, exhibit)
