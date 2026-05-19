from datetime import datetime, timezone, timedelta

import pytest

from app.models.enums import SessionStatus
from app.models.game_state import GameState
from app.repositories.memory_repo import MemorySessionRepository
from app.services.game_service import GameService, SessionExpiredError


@pytest.fixture(autouse=True)
def _reset_repo():
    """Reset the singleton repo before each test."""
    repo = MemorySessionRepository.get_instance()
    repo._store.clear()
    yield
    repo._store.clear()


def _make_state(session_id: str, hours_ago: float = 0) -> GameState:
    """Create a GameState with updated_at set to `hours_ago` hours in the past."""
    state = GameState(
        session_id=session_id,
        status=SessionStatus.ALIVE,
    )
    state.updated_at = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
    return state


class TestIsExpired:
    def test_returns_false_for_nonexistent_session(self):
        repo = MemorySessionRepository.get_instance()
        assert repo.is_expired("does-not-exist") is False

    def test_returns_true_for_expired_session(self):
        repo = MemorySessionRepository.get_instance()
        state = _make_state("expired-1", hours_ago=7)
        repo._store["expired-1"] = state
        assert repo.is_expired("expired-1") is True

    def test_returns_false_for_active_session(self):
        repo = MemorySessionRepository.get_instance()
        state = _make_state("active-1", hours_ago=1)
        repo._store["active-1"] = state
        assert repo.is_expired("active-1") is False

    def test_does_not_delete_session(self):
        repo = MemorySessionRepository.get_instance()
        state = _make_state("expired-2", hours_ago=7)
        repo._store["expired-2"] = state
        repo.is_expired("expired-2")
        assert "expired-2" in repo._store


class TestCleanupExpired:
    def test_removes_expired_keeps_active(self):
        repo = MemorySessionRepository.get_instance()
        repo._store["expired-a"] = _make_state("expired-a", hours_ago=7)
        repo._store["active-b"] = _make_state("active-b", hours_ago=0.5)
        repo._store["expired-c"] = _make_state("expired-c", hours_ago=8)

        removed = repo.cleanup_expired()

        assert removed == 2
        assert "expired-a" not in repo._store
        assert "expired-c" not in repo._store
        assert "active-b" in repo._store

    def test_returns_count(self):
        repo = MemorySessionRepository.get_instance()
        repo._store["e1"] = _make_state("e1", hours_ago=10)
        repo._store["e2"] = _make_state("e2", hours_ago=8)
        assert repo.cleanup_expired() == 2

    def test_returns_zero_when_no_expired(self):
        repo = MemorySessionRepository.get_instance()
        repo._store["a1"] = _make_state("a1", hours_ago=1)
        repo._store["a2"] = _make_state("a2", hours_ago=2)
        assert repo.cleanup_expired() == 0


class TestBoundaryConditions:
    def test_session_at_6h_minus_1s_is_not_expired(self):
        repo = MemorySessionRepository.get_instance()
        state = _make_state("boundary", hours_ago=6 - (1 / 3600))  # 6h - 1s
        repo._store["boundary"] = state
        assert repo.is_expired("boundary") is False

    def test_session_at_6h_plus_1s_is_expired(self):
        repo = MemorySessionRepository.get_instance()
        state = _make_state("boundary", hours_ago=6 + (1 / 3600))  # 6h + 1s
        repo._store["boundary"] = state
        assert repo.is_expired("boundary") is True


class TestProcessTurnExpiredSession:
    def test_raises_session_expired_error(self):
        repo = MemorySessionRepository.get_instance()
        repo._store["expired-turn"] = _make_state("expired-turn", hours_ago=7)

        svc = GameService()
        with pytest.raises(SessionExpiredError, match="Session expired"):
            svc.process_turn("expired-turn", "REST")

    def test_raises_value_error_for_nonexistent(self):
        svc = GameService()
        with pytest.raises(ValueError, match="not found"):
            svc.process_turn("never-existed", "REST")


class TestGetStateExpiredSession:
    def test_raises_session_expired_error(self):
        repo = MemorySessionRepository.get_instance()
        repo._store["expired-state"] = _make_state("expired-state", hours_ago=7)

        svc = GameService()
        with pytest.raises(SessionExpiredError, match="Session expired"):
            svc.get_state("expired-state")

    def test_returns_none_for_nonexistent(self):
        svc = GameService()
        assert svc.get_state("never-existed") is None
