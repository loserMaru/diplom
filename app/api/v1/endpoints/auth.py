from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.v1.deps import get_db
from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.crud import user as crud_user
from app.models.user import User
from app.schemas.user import UserPublic, UserCreate

router = APIRouter()


@router.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.email == form_data.username)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(subject=user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED, )
async def register(
        user_in: UserCreate,
        db: AsyncSession = Depends(get_db),
):
    existing_user = await crud_user.get_by_email(db, str(user_in.email))

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = await crud_user.create(db, data=user_in)
    return user
