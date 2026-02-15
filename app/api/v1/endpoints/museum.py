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
from app.schemas.museum import MuseumCreate, MuseumPublic, MuseumUpdate, MuseumSinglePublic
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


@router.get("/", response_model=list[MuseumPublic])
async def get_museums(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        q: str | None = Query(None, min_length=1),
):
    options = [
        selectinload(Museum.audios),
        selectinload(Museum.images),
        selectinload(Museum.exhibits).selectinload(Exhibit.images),
    ]

    if q:
        museums = await search_museums(
            db=db,
            query=q,
            skip=skip,
            limit=limit,
            options=options,
        )
    else:
        museums = await get_list(
            db=db,
            model=Museum,
            skip=skip,
            limit=limit,
            options=options,
        )

    museum_ids = [m.id for m in museums]
    stats_map = await get_museums_rating_stats_bulk(db, museum_ids)

    for museum in museums:
        stats = stats_map.get(museum.id)

        if stats:
            museum.rating_count = stats["rating_count"]
            museum.rating_avg = stats["rating_avg"]
            museum.rating_distribution = stats["rating_distribution"]
        else:
            museum.rating_count = 0
            museum.rating_avg = 0.0
            museum.rating_distribution = {i: 0 for i in range(1, 6)}

    return museums


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
async def get_museum_with_ratings(museum_id: int, db: AsyncSession = Depends(get_db)):
    # Получаем музей с загрузкой аудио, изображений, экспонатов
    result = await db.execute(
        select(Museum)
        .options(
            selectinload(Museum.audios),
            selectinload(Museum.images),
            selectinload(Museum.exhibits).selectinload(Exhibit.images),
        )
        .where(Museum.id == museum_id)
    )
    museum: Museum | None = result.scalar_one_or_none()

    if not museum:
        raise HTTPException(status_code=404, detail="Museum not found")

    # Получаем все рейтинги для музея вместе с именем и фамилией пользователя
    result = await db.execute(
        select(MuseumRating, UserProfile)
        .join(User, MuseumRating.user_id == User.id)
        .join(UserProfile, UserProfile.user_id == User.id)
        .where(MuseumRating.museum_id == museum_id)
    )

    ratings: list[MuseumRatingPublic] = []
    for rating, profile in result.all():
        ratings.append(
            MuseumRatingPublic(
                id=rating.id,
                rating=rating.rating,
                comment=rating.comment,
                museum_id=rating.museum_id,
                first_name=profile.first_name,
                last_name=profile.last_name,
            )
        )

    # Формируем ответ
    return MuseumSinglePublic(
        id=museum.id,
        name=museum.name,
        description=museum.description,
        audios=[MuseumAudioForMuseum.from_orm(audio) for audio in museum.audios],
        images=[MuseumImageForMuseum.from_orm(img) for img in museum.images],
        exhibits=[ExhibitForMuseum.from_orm(exh) for exh in museum.exhibits],
        rating_avg=museum.rating_avg,
        rating_count=museum.rating_count,
        rating_distribution=getattr(museum, "rating_distribution", {i: 0 for i in range(1, 6)}),
        ratings=ratings
    )
