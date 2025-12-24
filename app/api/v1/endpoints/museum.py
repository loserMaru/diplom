from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.v1.deps import get_db
from app.models.museum import Museum
from app.schemas.museum import MuseumCreate, MuseumPublic

router = APIRouter()


@router.post("/", response_model=MuseumPublic)
async def create_museum(
    data: MuseumCreate,
    db: AsyncSession = Depends(get_db),
):
    museum = Museum(
        name=data.name,
        description=data.description,
    )
    db.add(museum)
    await db.commit()

    stmt = (
        select(Museum)
        .where(Museum.id == museum.id)
        .options(selectinload(Museum.images))
    )
    result = await db.execute(stmt)
    museum = result.scalar_one()

    return museum

@router.get("/", response_model=list[MuseumPublic])
async def get_museums(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    stmt = (select(Museum).offset(skip).limit(limit).options(selectinload(Museum.images)))
    result = await db.execute(stmt)
    return result.scalars().all()
