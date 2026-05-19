import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.repositories.memory_repo import MemorySessionRepository
from app.routers import game_router, session_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async def cleanup_loop() -> None:
        while True:
            await asyncio.sleep(900)  # 15 minutes
            removed = MemorySessionRepository.get_instance().cleanup_expired()
            if removed:
                logger.info("Cleaned up %d expired session(s)", removed)

    task = asyncio.create_task(cleanup_loop())
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


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