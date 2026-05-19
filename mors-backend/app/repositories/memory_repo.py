from datetime import datetime, timezone, timedelta
from typing import Self

from app.core.config import settings
from app.models.game_state import GameState
from app.repositories.base import AbstractSessionRepository


class MemorySessionRepository:
    _instance: Self | None = None

    def __init__(self) -> None:
        self._store: dict[str, GameState] = {}

    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get(self, session_id: str) -> GameState | None:
        state = self._store.get(session_id)
        if state is None:
            return None
        if self._is_expired(state):
            del self._store[session_id]
            return None
        return state

    def save(self, state: GameState) -> None:
        state.updated_at = datetime.now(timezone.utc)
        self._store[state.session_id] = state

    def delete(self, session_id: str) -> None:
        self._store.pop(session_id, None)

    def list_all(self) -> list[GameState]:
        return [
            s for s in self._store.values() if not self._is_expired(s)
        ]

    def cleanup_expired(self) -> int:
        expired = [
            sid for sid, s in self._store.items() if self._is_expired(s)
        ]
        for sid in expired:
            del self._store[sid]
        return len(expired)

    def _is_expired(self, state: GameState) -> bool:
        ttl = timedelta(hours=settings.session_ttl_hours)
        return datetime.now(timezone.utc) - state.updated_at > ttl

    def is_expired(self, session_id: str) -> bool:
        """Check if a session exists and is expired without deleting it.

        Returns False if session does not exist (not expired, just missing).
        """
        state = self._store.get(session_id)
        if state is None:
            return False
        return self._is_expired(state)