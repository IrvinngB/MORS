from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models.game_state import GameState
from app.models.roles_registry import ROLES
from app.repositories.memory_repo import MemorySessionRepository


class SessionService:
    def __init__(self) -> None:
        self._repo = MemorySessionRepository.get_instance()

    def create_session(self, role_id: str = "") -> GameState:
        state = GameState(
            session_id=str(uuid4()),
            role=role_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        # Apply role deltas if a valid role is specified
        if role_id and role_id in ROLES:
            role_def = ROLES[role_id]
            state.player.hp = max(0.0, min(100.0, state.player.hp + role_def.hp_delta))
            state.player.stamina = max(0.0, min(100.0, state.player.stamina + role_def.stamina_delta))
            state.player.willpower = max(0.0, min(100.0, state.player.willpower + role_def.willpower_delta))

            # Merge starting equipment
            for item_key, item_delta in role_def.starting_equipment.items():
                if hasattr(state.consumables, item_key):
                    current = getattr(state.consumables, item_key)
                    if isinstance(current, float):
                        setattr(state.consumables, item_key, min(100.0, current + item_delta))
                    else:
                        setattr(state.consumables, item_key, current + item_delta)

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
