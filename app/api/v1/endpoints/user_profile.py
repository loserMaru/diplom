from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.v1.deps import get_db, get_current_user
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate, UserProfilePublic

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", response_model=UserProfilePublic)
async def get_my_profile(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )
    return profile


@router.post("/", response_model=UserProfilePublic, status_code=status.HTTP_201_CREATED)
async def create_my_profile(
        profile_in: UserProfileCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    # Проверка, что профиль еще не создан
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists"
        )

    profile = UserProfile(
        user_id=current_user.id,
        first_name=profile_in.first_name,
        last_name=profile_in.last_name,
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


@router.patch("/", response_model=UserProfilePublic)
async def update_my_profile(
        profile_in: UserProfileUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
        )

    profile.first_name = profile_in.first_name
    profile.last_name = profile_in.last_name

    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile
