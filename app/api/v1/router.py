from fastapi import APIRouter

from app.api.v1.endpoints import (
    users, auth,
    museum,
    museum_images,
    exhibit,
    exhibit_images,
    exhibit_models,
    museum_audios
)

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(museum.router, prefix="/museum", tags=["museum"])
api_router.include_router(museum_audios.router, prefix="/museum-audio", tags=["Museum Audios"])
api_router.include_router(museum_images.router, prefix="/museum-images", tags=["Museum Images"])
api_router.include_router(exhibit.router, prefix="/exhibit", tags=["Exhibit"])
api_router.include_router(exhibit_images.router, prefix="/exhibit-images", tags=["Exhibit Images"])
api_router.include_router(exhibit_models.router, prefix="/exhibit-models", tags=["Exhibit Models"])
