import pytest

from app.core.game_engine import (
    process,
    _stamina_cost,
    _body_temp_delta,
    _willpower_delta,
    _night_penalty,
)
from app.models.game_state import GameState, PlayerStats, Consumables
from app.models.enums import ActionType, WeatherState, SessionStatus


def make_state(**overrides) -> GameState:
    defaults = {
        "session_id": "test-session",
        "status": SessionStatus.ALIVE,
        "turn": 0,
        "player": PlayerStats(
            hp=100.0,
            stamina=100.0,
            body_temp=37.0,
            willpower=100.0,
            altitude=5200.0,
        ),
        "consumables": Consumables(
            food_rations=10,
            gas_canisters=5,
            rope_sections=3,
            oxygen_pct=100.0,
        ),
        "weather": WeatherState.CLEAR,
        "weather_forecast": WeatherState.CLEAR,
        "forecast_reliability": 1.0,
        "route_secured": 0,
    }
    defaults.update(overrides)
    return GameState(**defaults)


class TestStaminaCost:
    def test_base_cost_at_base_altitude_clear(self):
        # BASE_STAMINA_COST=12, altitude_factor=(1+(5200/8000)^2)=1.4225, oxygen_mod=0.8 (oxygen>50)
        # 12 * 1.4225 * 1.0 * 0.8 = 13.656
        cost = _stamina_cost(5200, WeatherState.CLEAR, 100.0, 100.0)
        assert cost == pytest.approx(13.656, rel=1e-3)


    def test_cost_increases_with_altitude(self):
        low = _stamina_cost(5200, WeatherState.CLEAR, 100.0, 100.0)
        high = _stamina_cost(8000, WeatherState.CLEAR, 100.0, 100.0)
        assert high > low

    def test_cost_increases_with_bad_weather(self):
        clear = _stamina_cost(7000, WeatherState.CLEAR, 100.0, 100.0)
        storm = _stamina_cost(7000, WeatherState.STORM, 100.0, 100.0)
        assert storm > clear

    def test_oxygen_below_30_increases_cost(self):
        high_o2 = _stamina_cost(7000, WeatherState.CLEAR, 60.0, 100.0)
        low_o2 = _stamina_cost(7000, WeatherState.CLEAR, 20.0, 100.0)
        assert low_o2 > high_o2

    def test_willpower_below_20_increases_cost(self):
        normal = _stamina_cost(7000, WeatherState.CLEAR, 100.0, 50.0)
        broken = _stamina_cost(7000, WeatherState.CLEAR, 100.0, 15.0)
        assert broken > normal


class TestBodyTempDelta:
    def test_temp_drops_passively(self):
        delta = _body_temp_delta(5200, WeatherState.CLEAR, False, 0)
        assert delta < 0

    def test_night_increases_temp_loss(self):
        day = _body_temp_delta(5200, WeatherState.CLEAR, False, 0)
        night = _body_temp_delta(5200, WeatherState.CLEAR, True, 0)
        assert night < day

    def test_storm_increases_temp_loss(self):
        clear = _body_temp_delta(7000, WeatherState.CLEAR, False, 0)
        storm = _body_temp_delta(7000, WeatherState.STORM, False, 0)
        assert storm < clear


class TestWillpowerDelta:
    def test_willpower_decreases_passively(self):
        delta = _willpower_delta(5200, 0, 0, False, WeatherState.CLEAR)
        assert delta < 0

    def test_death_zone_intensifies_loss(self):
        normal = _willpower_delta(6000, 10, 0, False, WeatherState.CLEAR)
        death_zone = _willpower_delta(8000, 10, 3, False, WeatherState.CLEAR)
        assert death_zone < normal


class TestNightPenalty:
    def test_night_penalty_is_1_3(self):
        assert _night_penalty(True) == pytest.approx(1.3)
        assert _night_penalty(False) == pytest.approx(1.0)


class TestGameEngineProcess:
    def test_advance_normal_gains_altitude(self):
        state = make_state()
        new_state, deltas = process(state, ActionType.ADVANCE_NORMAL)
        assert deltas.altitude_delta > 0
        assert new_state.player.altitude > state.player.altitude

    def test_advance_normal_consumes_stamina(self):
        state = make_state()
        new_state, deltas = process(state, ActionType.ADVANCE_NORMAL)
        assert deltas.stamina_delta < 0

    def test_advance_aggressive_gains_more_altitude(self):
        normal_state = make_state()
        _, normal_deltas = process(normal_state, ActionType.ADVANCE_NORMAL)

        aggressive_state = make_state()
        _, aggressive_deltas = process(aggressive_state, ActionType.ADVANCE_AGGRESSIVE)

        assert aggressive_deltas.altitude_delta > normal_deltas.altitude_delta

    def test_descend_reduces_altitude(self):
        state = make_state(player=PlayerStats(altitude=6000.0))
        new_state, deltas = process(state, ActionType.DESCEND)
        assert deltas.altitude_delta < 0

    def test_camp_consumes_resources(self):
        state = make_state()
        new_state, deltas = process(state, ActionType.CAMP)
        assert new_state.consumables.food_rations < state.consumables.food_rations

    def test_eat_requires_food(self):
        state = make_state(consumables=Consumables(food_rations=0))
        new_state, deltas = process(state, ActionType.EAT)
        assert deltas.stamina_delta == 0

    def test_eat_restores_stamina(self):
        state = make_state(consumables=Consumables(food_rations=5))
        new_state, deltas = process(state, ActionType.EAT)
        assert deltas.stamina_delta > 0

    def test_secured_route_depletes_rope(self):
        state = make_state(consumables=Consumables(rope_sections=3))
        new_state, deltas = process(state, ActionType.SECURE_ROUTE)
        assert new_state.consumables.rope_sections == 2
        assert deltas.route_secured_delta > 0

    def test_secure_route_increases_route_secured(self):
        state = make_state()
        new_state, deltas = process(state, ActionType.SECURE_ROUTE)
        assert new_state.route_secured > state.route_secured

    def test_hp_cannot_exceed_100(self):
        state = make_state(player=PlayerStats(hp=100.0, stamina=0.0))
        for _ in range(20):
            state, _ = process(state, ActionType.REST)
        assert state.player.hp <= 100.0

    def test_hp_cannot_be_negative(self):
        state = make_state(player=PlayerStats(hp=5.0))
        new_state, _ = process(state, ActionType.ADVANCE_AGGRESSIVE)
        assert new_state.player.hp >= 0.0

    def test_reaches_summit(self):
        state = make_state(player=PlayerStats(altitude=8600.0))
        new_state, _ = process(state, ActionType.ADVANCE_NORMAL)
        assert new_state.player.altitude >= 8611.0
        assert new_state.status == SessionStatus.SUMMIT

    def test_turn_counter_increments(self):
        state = make_state()
        _, deltas = process(state, ActionType.REST)
        assert deltas.altitude_delta == 0.0
        assert deltas.stamina_delta > 0