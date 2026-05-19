import pytest
from unittest.mock import patch

from app.services.event_service import (
    roll_event,
    _base_event_chance,
    _can_second_wind,
    EVENT_DEFINITIONS,
)
from app.models.enums import EventType, SessionStatus
from app.models.game_state import GameState, PlayerStats, Consumables


def make_state(**overrides) -> GameState:
    defaults = {
        "session_id": "test-event-session",
        "status": SessionStatus.ALIVE,
        "turn": 0,
        "player": PlayerStats(
            hp=100.0,
            stamina=100.0,
            body_temp=37.0,
            willpower=100.0,
            altitude=6000.0,
        ),
        "consumables": Consumables(
            food_rations=10,
            gas_canisters=5,
            rope_sections=3,
            oxygen_pct=100.0,
        ),
        "weather": "CLEAR",
        "weather_forecast": "CLEAR",
        "forecast_reliability": 1.0,
        "route_secured": 0,
        "turns_without_stamina_recovery": 0,
    }
    defaults.update(overrides)
    return GameState(**defaults)


class TestBaseEventChance:
    def test_base_chance_at_sea_level(self):
        state = make_state(player=PlayerStats(altitude=5200.0, turns_above_8000=0))
        assert _base_event_chance(state) == pytest.approx(0.15)

    def test_chance_increases_with_death_zone(self):
        state = make_state(player=PlayerStats(altitude=8500.0, turns_above_8000=3))
        assert _base_event_chance(state) == pytest.approx(0.30)

    def test_chance_capped_at_50_percent(self):
        state = make_state(player=PlayerStats(altitude=9000.0, turns_above_8000=20))
        assert _base_event_chance(state) == pytest.approx(0.50)


class TestCanSecondWind:
    def test_false_before_10_turns(self):
        state = make_state(turns_without_stamina_recovery=9)
        assert _can_second_wind(state) is False

    def test_true_at_10_turns(self):
        state = make_state(turns_without_stamina_recovery=10)
        assert _can_second_wind(state) is True

    def test_true_above_10_turns(self):
        state = make_state(turns_without_stamina_recovery=15)
        assert _can_second_wind(state) is True


class TestRollEvent:
    def test_returns_none_when_no_roll(self):
        state = make_state()
        with patch("random.random", return_value=1.0):
            result = roll_event(state)
        assert result is None

    def test_returns_none_for_dead_session(self):
        state = make_state(status=SessionStatus.DEAD)
        result = roll_event(state)
        assert result is None

    def test_returns_none_for_summit_session(self):
        state = make_state(status=SessionStatus.SUMMIT)
        result = roll_event(state)
        assert result is None

    def test_returns_none_for_abandoned_session(self):
        state = make_state(status=SessionStatus.ABANDONED)
        result = roll_event(state)
        assert result is None

    def test_roll_event_returns_dict_with_event_type_and_narrative(self):
        state = make_state()
        with patch("random.random", return_value=0.0):
            result = roll_event(state)
        assert result is not None
        assert "event_type" in result
        assert "narrative" in result

    def test_roll_event_includes_deltas(self):
        state = make_state()
        with patch("random.random", return_value=0.0):
            result = roll_event(state)
        assert result is not None
        assert any(
            key in result
            for key in ("hp_delta", "stamina_delta", "willpower_delta", "oxygen_delta", "temp_delta", "rope_delta")
        )

    def test_second_wind_requires_10_turns(self):
        state_under = make_state(turns_without_stamina_recovery=9)
        state_exact = make_state(turns_without_stamina_recovery=10)

        second_wind_triggered_under = False
        second_wind_triggered_exact = False

        for _ in range(50):
            with patch("random.random", return_value=0.05):
                r_under = roll_event(state_under)
                r_exact = roll_event(state_exact)
                if r_under and r_under.get("event_type") == EventType.SECOND_WIND.value:
                    second_wind_triggered_under = True
                if r_exact and r_exact.get("event_type") == EventType.SECOND_WIND.value:
                    second_wind_triggered_exact = True

        assert not second_wind_triggered_under, "SECOND_WIND should not trigger under 10 turns"
        assert second_wind_triggered_exact, "SECOND_WIND should be possible at exactly 10 turns"

    def test_second_wind_has_positive_deltas(self):
        state = make_state(turns_without_stamina_recovery=15)
        for _ in range(100):
            with patch("random.random", return_value=0.05):
                result = roll_event(state)
                if result and result.get("event_type") == EventType.SECOND_WIND.value:
                    assert result.get("stamina_delta", 0) > 0
                    assert result.get("willpower_delta", 0) > 0
                    return
        pytest.fail("SECOND_WIND event not triggered in 100 attempts")


class TestEventDefinitions:
    def test_all_10_events_defined(self):
        assert len(EVENT_DEFINITIONS) == 10

    def test_all_events_have_narrative(self):
        for event_type, data in EVENT_DEFINITIONS.items():
            assert "narrative" in data
            assert isinstance(data["narrative"], str)
            assert len(data["narrative"]) > 0

    def test_all_events_have_at_least_one_effect(self):
        effect_keys = {"hp_delta", "stamina_delta", "willpower_delta", "oxygen_delta", "temp_delta", "rope_delta"}
        for event_type, data in EVENT_DEFINITIONS.items():
            has_effect = any(k in data for k in effect_keys)
            assert has_effect, f"{event_type} has no effect defined"

    def test_second_wind_is_positive(self):
        data = EVENT_DEFINITIONS[EventType.SECOND_WIND]
        assert data.get("stamina_delta", 0) > 0
        assert data.get("willpower_delta", 0) > 0

    def test_critical_events_are_harmful(self):
        critical = [EventType.HALLUCINATION, EventType.PULMONARY_EDEMA, EventType.FROSTBITE]
        for event_type in critical:
            data = EVENT_DEFINITIONS[event_type]
            is_harmful = (
                data.get("hp_delta", 0) < 0
                or data.get("stamina_delta", 0) < 0
                or data.get("willpower_delta", 0) < 0
            )
            assert is_harmful, f"{event_type} should have harmful effects"

    def test_partner_vision_has_no_mechanical_effect(self):
        data = EVENT_DEFINITIONS[EventType.PARTNER_VISION]
        mechanical_keys = ["hp_delta", "stamina_delta", "temp_delta", "oxygen_delta"]
        has_mechanical = any(k in data for k in mechanical_keys)
        assert not has_mechanical, "PARTNER_VISION should have no mechanical effect"

    def test_distinct_avalanche_low_willpower_impact(self):
        data = EVENT_DEFINITIONS[EventType.DISTANT_AVALANCHE]
        assert data.get("willpower_delta", 0) == -15

    def test_o2_regulator_fail_drops_oxygen(self):
        data = EVENT_DEFINITIONS[EventType.O2_REGULATOR_FAIL]
        assert data.get("oxygen_delta", 0) == -100


class TestEventDistribution:
    def test_above_8000_favors_critical_events(self):
        state = make_state(player=PlayerStats(altitude=8200.0, turns_above_8000=2))
        event_counts = {et.value: 0 for et in EventType}

        for _ in range(200):
            with patch("random.random", return_value=0.0):
                result = roll_event(state)
                if result:
                    event_counts[result["event_type"]] += 1

        critical_hits = sum(event_counts.get(et.value, 0) for et in [EventType.HALLUCINATION, EventType.PULMONARY_EDEMA, EventType.FROSTBITE])
        non_critical_hits = sum(event_counts.get(et.value, 0) for et in [EventType.DISTANT_AVALANCHE, EventType.WIND_GUST, EventType.O2_REGULATOR_FAIL, EventType.TENT_COLLAPSE, EventType.PARTNER_VISION, EventType.EQUIPMENT_DROP])

        assert critical_hits > non_critical_hits, "Above 8000m, critical events should dominate"

    def test_below_8000_no_pulmonary_edema_weight(self):
        state = make_state(player=PlayerStats(altitude=6000.0, turns_above_8000=0))
        pulmonary_hits = 0

        for _ in range(100):
            with patch("random.random", return_value=0.0):
                result = roll_event(state)
                if result and result.get("event_type") == EventType.PULMONARY_EDEMA.value:
                    pulmonary_hits += 1

        assert pulmonary_hits == 0, "PULMONARY_EDEMA should not appear below 8000m"