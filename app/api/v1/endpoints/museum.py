from fastapi import Depends, APIRouter, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from app.api.v1.deps import get_db, get_current_user
from app.crud.base import create_with_relations, get_list
from app.crud.museums import get_museum, update_museum, delete_museum, search_museums, get_museums_rating_stats_bulk
from app.models import MuseumRating, User, UserProfile
from app.models.exhibit import Exhibit
from app.models.museum import Museum
from app.schemas.museum import MuseumCreate, MuseumPublic, MuseumUpdate, MuseumSinglePublic, MuseumWithStats
from app.schemas.museum_audios import MuseumAudioForMuseum
from app.schemas.museum_images import MuseumImageForMuseum
from app.schemas.museum_ratings import MuseumRatingPublic
from app.schemas.shared import ExhibitForMuseum

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", response_model=MuseumPublic)
async def create_museum(
        data: MuseumCreate,
        db: AsyncSession = Depends(get_db),
):
    return await create_with_relations(
        db=db,
        model=Museum,
        data=data,
        load=[Museum.audios, Museum.images, Museum.exhibits],
    )


@router.get("/", response_model=list[MuseumWithStats])
async def get_museums(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    museums = await get_list(
        db=db,
        model=Museum,
        skip=skip,
        limit=limit,
        options=[
            selectinload(Museum.audios),
            selectinload(Museum.images),
            selectinload(Museum.exhibits).selectinload(Exhibit.images),
        ],
    )

    museum_ids = [m.id for m in museums]
    stats_map = await get_museums_rating_stats_bulk(db, museum_ids)

    result = []
    for museum in museums:
        stats = stats_map.get(museum.id, {
            "rating_avg": 0.0,
            "rating_count": 0,
            "rating_distribution": {i: 0 for i in range(1, 6)}
        })

        result.append(
            MuseumWithStats(
                id=museum.id,
                name=museum.name,
                description=museum.description,
                audios=museum.audios,
                images=museum.images,
                exhibits=museum.exhibits,
                rating_avg=stats["rating_avg"],
                rating_count=stats["rating_count"],
                rating_distribution=stats["rating_distribution"],
            )
        )

    return result


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

    return await update_museum(db, museum, data=museum_in)


@router.delete("/{museum_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_museum(
        museum_id: int,
        db: AsyncSession = Depends(get_db),
):
    museum = await get_museum(db, museum_id)
    if not museum:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Museum not found.",
        )

    return await delete_museum(db, museum)


@router.get("/{museum_id}", response_model=MuseumSinglePublic)
async def get_museum_with_ratings(
        museum_id: int,
        db: AsyncSession = Depends(get_db)
):
    # 1. музей
    result = await db.execute(
        select(Museum)
        .options(
            selectinload(Museum.audios),
            selectinload(Museum.images),
            selectinload(Museum.exhibits),
        )
        .where(Museum.id == museum_id)
    )
    museum = result.scalar_one_or_none()

    if not museum:
        raise HTTPException(status_code=404, detail="Museum not found")

    # 2. статистика
    stats_map = await get_museums_rating_stats_bulk(db, [museum_id])
    stats = stats_map.get(museum_id, {
        "rating_avg": 0.0,
        "rating_count": 0,
        "rating_distribution": {i: 0 for i in range(1, 6)}
    })

    # 3. отзывы + профиль
    result = await db.execute(
        select(MuseumRating, UserProfile)
        .join(User, User.id == MuseumRating.user_id)
        .outerjoin(UserProfile, UserProfile.user_id == User.id)
        .where(MuseumRating.museum_id == museum_id)
    )

    ratings = [
        MuseumRatingPublic(
            id=r.id,
            rating=r.rating,
            comment=r.comment,
            museum_id=r.museum_id,
            first_name=p.first_name if p else None,
            last_name=p.last_name if p else None,
        )
        for r, p in result.all()
    ]

    # 4. финальный ответ
    return MuseumSinglePublic(
        id=museum.id,
        name=museum.name,
        description=museum.description,
        audios=museum.audios,
        images=museum.images,
        exhibits=museum.exhibits,
        rating_avg=stats["rating_avg"],
        rating_count=stats["rating_count"],
        rating_distribution=stats["rating_distribution"],
        ratings=ratings
    )
