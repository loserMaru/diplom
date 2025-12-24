from fastapi import APIRouter

from app.api.v1.endpoints import users, auth, museum, museum_images

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(museum.router, prefix="/museum", tags=["museum"])
api_router.include_router(museum_images.router, prefix="/museum-images", tags=["Museum Images"])
