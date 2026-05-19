"""Tests for backward compatibility: no role = classic, invalid role = 400."""
import pytest
from fastapi.testclient import TestClient

from app.main import api
from app.models.roles_registry import ROLES
from app.services.game_service import GameService
from app.repositories.memory_repo import MemorySessionRepository


client = TestClient(api)


class TestBackwardCompatibility:
    """No role provided = classic behavior, all defaults unchanged."""

    def test_new_game_no_role_returns_empty_role(self):
        """POST /game/new with no body should create game with role=""."""
        response = client.post("/game/new")
        assert response.status_code == 201
        data = response.json()
        assert data["state"]["role"] == ""

    def test_new_game_empty_role_returns_empty_role(self):
        """POST /game/new with {\"role\": \"\"} should create game with role=""."""
        response = client.post("/game/new", json={"role": ""})
        assert response.status_code == 201
        data = response.json()
        assert data["state"]["role"] == ""

    def test_classic_game_has_base_stats(self):
        """Classic game (no role) should have base HP=100, stamina=100, willpower=100."""
        service = GameService()
        state, _ = service.new_game(role_id="")
        assert state.player.hp == 100.0
        assert state.player.stamina == 100.0
        assert state.player.willpower == 100.0
        assert state.role == ""

    def test_classic_game_has_base_equipment(self):
        """Classic game should have default consumables."""
        service = GameService()
        state, _ = service.new_game(role_id="")
        assert state.consumables.food_rations == 10
        assert state.consumables.gas_canisters == 5
        assert state.consumables.rope_sections == 3
        assert state.consumables.oxygen_pct == 100.0

    def test_classic_game_forecast_reliability_is_1_0(self):
        """Classic game should start with forecast_reliability = 1.0."""
        service = GameService()
        state, _ = service.new_game(role_id="")
        assert state.forecast_reliability == 1.0

    def test_classic_game_free_heal_unused(self):
        """Classic game should have free_heal_used = False."""
        service = GameService()
        state, _ = service.new_game(role_id="")
        assert state.free_heal_used is False


class TestInvalidRole:
    """Invalid role should return 400 Bad Request."""

    def test_invalid_role_returns_400(self):
        """POST /game/new with invalid role should return 400."""
        response = client.post("/game/new", json={"role": "invalid_role"})
        assert response.status_code == 400
        assert "Unknown role: invalid_role" in response.json()["detail"]

    def test_unknown_role_returns_400_with_message(self):
        """Error message should include the invalid role name."""
        response = client.post("/game/new", json={"role": "ninja"})
        assert response.status_code == 400
        assert "ninja" in response.json()["detail"]


class TestValidRoleCreation:
    """Valid role should create game with correct modifiers."""

    def test_valid_role_returns_display_name_and_difficulty(self):
        """POST /game/new with valid role should return role_display_name and role_difficulty."""
        response = client.post("/game/new", json={"role": "sherpa"})
        assert response.status_code == 201
        data = response.json()
        assert data["role_display_name"] == "Sherpa"
        assert data["role_difficulty"] == "Easy"

    def test_all_valid_roles_create_successfully(self):
        """All 5 roles should create a game successfully."""
        for role_id in ROLES:
            response = client.post("/game/new", json={"role": role_id})
            assert response.status_code == 201, f"Role {role_id} failed"
            data = response.json()
            assert data["state"]["role"] == role_id
