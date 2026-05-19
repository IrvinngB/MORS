from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import game_router, session_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


api = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(game_router)
api.include_router(session_router)


@api.get("/health")
async def health():
    return {"status": "ok"}