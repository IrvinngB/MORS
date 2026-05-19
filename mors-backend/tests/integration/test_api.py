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


class TestNewGame:
    def test_new_game_returns_201(self, client):
        response = client.post("/game/new")
        assert response.status_code == 201

    def test_new_game_returns_session_id(self, client):
        response = client.post("/game/new")
        data = response.json()
        assert "session_id" in data
        assert len(data["session_id"]) == 36

    def test_new_game_returns_state(self, client):
        response = client.post("/game/new")
        data = response.json()
        assert "state" in data
        assert data["state"]["status"] == "ALIVE"
        assert data["state"]["turn"] == 0

    def test_new_game_returns_narrative(self, client):
        response = client.post("/game/new")
        data = response.json()
        assert "narrative" in data
        assert len(data["narrative"]) > 0

    def test_new_game_player_has_correct_defaults(self, client):
        response = client.post("/game/new")
        player = response.json()["state"]["player"]
        assert player["hp"] == 100.0
        assert player["stamina"] == 100.0
        assert player["body_temp"] == 37.0
        assert player["willpower"] == 100.0
        assert player["altitude"] == 5200.0

    def test_new_game_creates_unique_session_ids(self, client):
        r1 = client.post("/game/new").json()["session_id"]
        r2 = client.post("/game/new").json()["session_id"]
        assert r1 != r2


class TestTurn:
    def test_turn_returns_200(self, client):
        new = client.post("/game/new").json()
        response = client.post("/game/turn", json={"session_id": new["session_id"], "action": "REST"})
        assert response.status_code == 200

    def test_turn_updates_turn_counter(self, client):
        new = client.post("/game/new").json()
        response = client.post("/game/turn", json={"session_id": new["session_id"], "action": "REST"})
        assert response.json()["new_state"]["turn"] == 1

    def test_turn_returns_deltas(self, client):
        new = client.post("/game/new").json()
        response = client.post("/game/turn", json={"session_id": new["session_id"], "action": "REST"})
        data = response.json()
        assert "deltas" in data
        assert "stamina_delta" in data["deltas"]

    def test_turn_rejects_invalid_action(self, client):
        new = client.post("/game/new").json()
        response = client.post("/game/turn", json={"session_id": new["session_id"], "action": "INVALID"})
        assert response.status_code == 422

    def test_turn_rejects_nonexistent_session(self, client):
        response = client.post("/game/turn", json={"session_id": "nonexistent-id", "action": "REST"})
        assert response.status_code == 422

    def test_turn_returns_narrative(self, client):
        new = client.post("/game/new").json()
        response = client.post("/game/turn", json={"session_id": new["session_id"], "action": "REST"})
        assert "narrative" in response.json()

    def test_advance_normal_changes_altitude(self, client):
        new = client.post("/game/new").json()
        response = client.post("/game/turn", json={"session_id": new["session_id"], "action": "ADVANCE_NORMAL"})
        altitude_delta = response.json()["deltas"]["altitude_delta"]
        assert altitude_delta > 0

    def test_eat_consumes_food(self, client):
        new = client.post("/game/new").json()
        food_before = new["state"]["consumables"]["food_rations"]
        response = client.post("/game/turn", json={"session_id": new["session_id"], "action": "EAT"})
        food_after = response.json()["new_state"]["consumables"]["food_rations"]
        assert food_after == food_before - 1

    def test_eat_with_no_food_no_effect(self, client):
        new = client.post("/game/new").json()
        state = new["state"]
        state["consumables"]["food_rations"] = 0
        client.post("/game/turn", json={"session_id": new["session_id"], "action": "EAT"})


class TestGetState:
    def test_get_state_returns_200(self, client):
        new = client.post("/game/new").json()
        response = client.get(f"/game/state/{new['session_id']}")
        assert response.status_code == 200

    def test_get_state_returns_state(self, client):
        new = client.post("/game/new").json()
        response = client.get(f"/game/state/{new['session_id']}")
        assert "state" in response.json()

    def test_get_state_nonexistent_returns_404(self, client):
        response = client.get("/game/state/nonexistent-id")
        assert response.status_code == 404


class TestDeleteSession:
    def test_delete_returns_204(self, client):
        new = client.post("/game/new").json()
        response = client.delete(f"/game/session/{new['session_id']}")
        assert response.status_code == 204

    def test_delete_removes_session(self, client):
        new = client.post("/game/new").json()
        client.delete(f"/game/session/{new['session_id']}")
        response = client.get(f"/game/state/{new['session_id']}")
        assert response.status_code == 404


class TestHealthCheck:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_ok(self, client):
        response = client.get("/health")
        assert response.json() == {"status": "ok"}


class TestGameEndConditions:
    def test_game_reaches_summit(self, client):
        new = client.post("/game/new").json()
        state = new["state"]
        state["player"]["altitude"] = 8600.0

        from app.services.game_service import GameService
        svc = GameService()
        svc._repo._store[new["session_id"]] = svc._repo.get(new["session_id"])
        svc._repo.get(new["session_id"]).player.altitude = 8600.0

        response = client.post("/game/turn", json={"session_id": new["session_id"], "action": "ADVANCE_NORMAL"})
        data = response.json()
        assert data["new_state"]["status"] == "SUMMIT"
        assert data["is_terminal"] is True

    def test_game_reaches_dead(self, client):
        new = client.post("/game/new").json()
        from app.services.game_service import GameService
        svc = GameService()
        svc._repo.get(new["session_id"]).player.hp = 5.0

        response = client.post("/game/turn", json={"session_id": new["session_id"], "action": "ADVANCE_AGGRESSIVE"})
        data = response.json()
        if data["is_terminal"]:
            assert data["new_state"]["status"] == "DEAD"


class TestListSessions:
    def test_list_sessions_returns_200(self, client):
        response = client.get("/game/sessions")
        assert response.status_code == 200

    def test_list_sessions_returns_count(self, client):
        client.post("/game/new")
        client.post("/game/new")
        response = client.get("/game/sessions")
        assert response.json()["count"] >= 2


class TestNarrative:
    def test_narrative_log_grows(self, client):
        new = client.post("/game/new").json()
        initial_log_len = len(new["state"]["narrative_log"])

        for _ in range(3):
            client.post("/game/turn", json={"session_id": new["session_id"], "action": "REST"})

        response = client.get(f"/game/state/{new['session_id']}")
        final_log_len = len(response.json()["state"]["narrative_log"])
        assert final_log_len > initial_log_len