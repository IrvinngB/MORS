from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models.game_state import GameState
from app.repositories.memory_repo import MemorySessionRepository


class SessionService:
    def __init__(self) -> None:
        self._repo = MemorySessionRepository.get_instance()

    def create_session(self) -> GameState:
        state = GameState(
            session_id=str(uuid4()),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        self._repo.save(state)
        return state

    def get_session(self, session_id: str) -> Optional[GameState]:
        return self._repo.get(session_id)

    def delete_session(self, session_id: str) -> bool:
        self._repo.delete(session_id)
        return True

    def list_sessions(self) -> list[GameState]:
        return self._repo.list_all()

    def cleanup_expired(self) -> int:
        return self._repo.cleanup_expired()