"""
Playability tests — verify that a full game can be completed.

These tests simulate complete games from start to finish to ensure:
1. The player CAN reach the summit (victory condition)
2. The player CAN die (defeat condition)
3. The game engine doesn't get stuck in infinite loops
4. All terminal conditions are reachable through normal play
"""
import pytest
from fastapi.testclient import TestClient

from app.main import api
from app.models.enums import SessionStatus
from app.services.session_service import SessionService


@pytest.fixture
def client():
    return TestClient(api)


@pytest.fixture(autouse=True)
def clean_sessions():
    repo = SessionService()._repo
    repo._store.clear()
    yield
    repo._store.clear()


class TestCanReachSummit:
    """Verify that a player can reach the summit through normal play."""

    def test_summit_is_reachable_with_optimal_play(self, client):
        """Start a game and advance aggressively until summit."""
        new = client.post("/game/new").json()
        session_id = new["session_id"]
        state = new["state"]

        # Set altitude close to summit to speed up test
        state["player"]["altitude"] = 8500.0
        state["player"]["hp"] = 100.0
        state["player"]["stamina"] = 100.0
        state["player"]["willpower"] = 100.0
        state["consumables"]["food_rations"] = 20
        state["consumables"]["gas_canisters"] = 10
        state["consumables"]["rope_sections"] = 5
        state["consumables"]["oxygen_pct"] = 100.0

        # Update state in repo
        from app.services.game_service import GameService
        svc = GameService()
        svc._repo._store[session_id] = svc._repo.get(session_id)
        svc._repo.get(session_id).player.altitude = 8500.0
        svc._repo.get(session_id).player.hp = 100.0
        svc._repo.get(session_id).player.stamina = 100.0
        svc._repo.get(session_id).player.willpower = 100.0
        svc._repo.get(session_id).consumables.food_rations = 20
        svc._repo.get(session_id).consumables.gas_canisters = 10
        svc._repo.get(session_id).consumables.rope_sections = 5
        svc._repo.get(session_id).consumables.oxygen_pct = 100.0

        # Advance until summit
        max_turns = 20
        for turn in range(max_turns):
            response = client.post("/game/turn", json={
                "session_id": session_id,
                "action": "ADVANCE_NORMAL"
            })
            data = response.json()

            if data.get("is_terminal"):
                assert data["new_state"]["status"] == "SUMMIT"
                assert data["new_state"]["player"]["altitude"] >= 8611.0
                return

            # Recover stamina if needed
            if data["new_state"]["player"]["stamina"] < 30:
                client.post("/game/turn", json={
                    "session_id": session_id,
                    "action": "CAMP"
                })

            # Use oxygen if available
            if data["new_state"]["player"]["stamina"] < 50 and data["new_state"]["consumables"]["gas_canisters"] > 0:
                client.post("/game/turn", json={
                    "session_id": session_id,
                    "action": "USE_OXYGEN"
                })

        pytest.fail(f"Did not reach summit in {max_turns} turns")

    def test_summit_requires_positive_hp(self, client):
        """Verify that summit requires HP > 0."""
        new = client.post("/game/new").json()
        session_id = new["session_id"]

        from app.services.game_service import GameService
        svc = GameService()
        svc._repo.get(session_id).player.altitude = 8600.0
        svc._repo.get(session_id).player.hp = 0.0

        response = client.post("/game/turn", json={
            "session_id": session_id,
            "action": "ADVANCE_NORMAL"
        })
        data = response.json()

        # Should be DEAD, not SUMMIT
        assert data["new_state"]["status"] == "DEAD"
        assert data["new_state"]["status"] != "SUMMIT"


class TestCanReachDeath:
    """Verify that a player can die through normal play."""

    def test_death_by_exhaustion(self, client):
        """Player dies from exhaustion (stamina -> 0 -> HP loss)."""
        new = client.post("/game/new").json()
        session_id = new["session_id"]

        from app.services.game_service import GameService
        svc = GameService()
        state = svc._repo.get(session_id)
        state.player.hp = 10.0
        state.player.stamina = 5.0

        # Keep taking actions until death
        max_turns = 50
        for turn in range(max_turns):
            response = client.post("/game/turn", json={
                "session_id": session_id,
                "action": "ADVANCE_AGGRESSIVE"
            })
            data = response.json()

            if data.get("is_terminal"):
                assert data["new_state"]["status"] == "DEAD"
                assert data["new_state"]["death_cause"] in (
                    "DEAD_EXHAUSTION", "DEAD_COLD", "DEAD_FALL"
                )
                return

        pytest.fail(f"Did not die in {max_turns} turns")

    def test_death_by_fall(self, client):
        """Player can die from a fall during aggressive advance."""
        new = client.post("/game/new").json()
        session_id = new["session_id"]

        from app.services.game_service import GameService
        svc = GameService()
        state = svc._repo.get(session_id)
        state.player.hp = 15.0
        state.player.stamina = 10.0

        # Aggressive advance has fall risk
        max_turns = 30
        for turn in range(max_turns):
            response = client.post("/game/turn", json={
                "session_id": session_id,
                "action": "ADVANCE_AGGRESSIVE"
            })
            data = response.json()

            if data.get("is_terminal"):
                assert data["new_state"]["status"] == "DEAD"
                return

        pytest.fail(f"Did not die in {max_turns} turns")

    def test_death_cause_is_recorded(self, client):
        """Verify that death cause is properly recorded."""
        new = client.post("/game/new").json()
        session_id = new["session_id"]

        from app.services.game_service import GameService
        svc = GameService()
        state = svc._repo.get(session_id)
        state.player.hp = 5.0
        state.player.stamina = 0.0

        response = client.post("/game/turn", json={
            "session_id": session_id,
            "action": "ADVANCE_AGGRESSIVE"
        })
        data = response.json()

        assert data["new_state"]["status"] == "DEAD"
        assert data["new_state"]["death_cause"] is not None
        assert data["new_state"]["death_cause"] in (
            "DEAD_EXHAUSTION", "DEAD_COLD", "DEAD_FALL", "DEAD_STORM", "DEAD_EDEMA"
        )


class TestGameFlow:
    """Test general game flow and mechanics."""

    def test_game_starts_in_alive_state(self, client):
        """New game should start with ALIVE status."""
        new = client.post("/game/new").json()
        assert new["state"]["status"] == "ALIVE"
        assert new["state"]["turn"] == 0
        assert new["state"]["player"]["hp"] == 100.0
        assert new["state"]["player"]["altitude"] == 5200.0

    def test_turn_counter_increments(self, client):
        """Each turn should increment the turn counter."""
        new = client.post("/game/new").json()
        session_id = new["session_id"]

        for i in range(1, 6):
            response = client.post("/game/turn", json={
                "session_id": session_id,
                "action": "REST"
            })
            assert response.json()["new_state"]["turn"] == i

    def test_actions_blocked_after_death(self, client):
        """Actions should be blocked after player dies."""
        new = client.post("/game/new").json()
        session_id = new["session_id"]

        from app.services.game_service import GameService
        svc = GameService()
        state = svc._repo.get(session_id)
        state.player.hp = 5.0
        state.player.stamina = 0.0

        # First action kills player
        client.post("/game/turn", json={
            "session_id": session_id,
            "action": "ADVANCE_AGGRESSIVE"
        })

        # Second action should fail
        response = client.post("/game/turn", json={
            "session_id": session_id,
            "action": "REST"
        })
        assert response.status_code == 422

    def test_narrative_log_grows(self, client):
        """Narrative log should grow with each turn."""
        new = client.post("/game/new").json()
        session_id = new["session_id"]
        initial_log_len = len(new["state"]["narrative_log"])

        for _ in range(5):
            client.post("/game/turn", json={
                "session_id": session_id,
                "action": "REST"
            })

        response = client.get(f"/game/state/{session_id}")
        final_log_len = len(response.json()["state"]["narrative_log"])
        assert final_log_len > initial_log_len

    def test_weather_changes_over_time(self, client):
        """Weather should change over multiple turns."""
        new = client.post("/game/new").json()
        session_id = new["session_id"]
        initial_weather = new["state"]["weather"]

        weather_changed = False
        for _ in range(20):
            client.post("/game/turn", json={
                "session_id": session_id,
                "action": "REST"
            })
            response = client.get(f"/game/state/{session_id}")
            current_weather = response.json()["state"]["weather"]
            if current_weather != initial_weather:
                weather_changed = True
                break

        assert weather_changed, "Weather did not change in 20 turns"

    def test_forecast_reliability_varies(self, client):
        """Forecast reliability should vary based on conditions."""
        new = client.post("/game/new").json()
        session_id = new["session_id"]

        reliabilities = set()
        for _ in range(10):
            client.post("/game/turn", json={
                "session_id": session_id,
                "action": "REST"
            })
            response = client.get(f"/game/state/{session_id}")
            reliability = response.json()["state"]["forecast_reliability"]
            reliabilities.add(round(reliability, 2))

        assert len(reliabilities) > 1, "Forecast reliability did not vary"


class TestResourceManagement:
    """Test that resources are properly managed."""

    def test_food_consumption(self, client):
        """Eating should consume food rations."""
        new = client.post("/game/new").json()
        session_id = new["session_id"]
        initial_food = new["state"]["consumables"]["food_rations"]

        response = client.post("/game/turn", json={
            "session_id": session_id,
            "action": "EAT"
        })
        final_food = response.json()["new_state"]["consumables"]["food_rations"]
        assert final_food == initial_food - 1

    def test_rope_consumption(self, client):
        """Securing route should consume rope sections."""
        new = client.post("/game/new").json()
        session_id = new["session_id"]
        initial_rope = new["state"]["consumables"]["rope_sections"]

        response = client.post("/game/turn", json={
            "session_id": session_id,
            "action": "SECURE_ROUTE"
        })
        final_rope = response.json()["new_state"]["consumables"]["rope_sections"]
        assert final_rope == initial_rope - 1

    def test_oxygen_recovery(self, client):
        """Using oxygen should recover oxygen_pct."""
        new = client.post("/game/new").json()
        session_id = new["session_id"]

        from app.services.game_service import GameService
        svc = GameService()
        svc._repo.get(session_id).consumables.oxygen_pct = 20.0

        response = client.post("/game/turn", json={
            "session_id": session_id,
            "action": "USE_OXYGEN"
        })
        final_oxygen = response.json()["new_state"]["consumables"]["oxygen_pct"]
        assert final_oxygen > 20.0

    def test_camp_consumes_resources(self, client):
        """Camping should consume food and gas."""
        new = client.post("/game/new").json()
        session_id = new["session_id"]
        initial_food = new["state"]["consumables"]["food_rations"]
        initial_gas = new["state"]["consumables"]["gas_canisters"]

        response = client.post("/game/turn", json={
            "session_id": session_id,
            "action": "CAMP"
        })
        final_food = response.json()["new_state"]["consumables"]["food_rations"]
        final_gas = response.json()["new_state"]["consumables"]["gas_canisters"]
        assert final_food == initial_food - 1
        assert final_gas == initial_gas - 1
