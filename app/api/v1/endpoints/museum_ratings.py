from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_db, get_current_user
from app.crud.museum_ratings import rate_museum, get_my_museum_ratings
from app.schemas.museum_ratings import MuseumRatingPublic

router = APIRouter(
    prefix="/museum-ratings",
    tags=["Museum Ratings"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/rate", status_code=status.HTTP_204_NO_CONTENT)
async def rate_museum_endpoint(
        museum_id: int,
        rating: int,
        comment: str | None = None,
        db: AsyncSession = Depends(get_db),
        user=Depends(get_current_user),
):
    await rate_museum(
        db=db,
        user_id=user.id,
        museum_id=museum_id,
        rating=rating,
        comment=comment,
    )


@router.get("/my-ratings", response_model=list[MuseumRatingPublic])
async def get_museum_ratings(
        db: AsyncSession = Depends(get_db),
        user=Depends(get_current_user),
):
    return await get_my_museum_ratings(db=db, user_id=user.id)
