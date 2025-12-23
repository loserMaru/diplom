from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.db.init_db import init_models

from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_models()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
