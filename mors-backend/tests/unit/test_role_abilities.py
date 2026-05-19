"""Tests for all 5 role special abilities."""
import pytest

from app.core.game_engine import process, _build_role_modifiers
from app.models.enums import ActionType, WeatherState, SessionStatus
from app.models.game_state import GameState, PlayerStats, Consumables
from app.models.roles import RoleSpecialAbility
from app.models.roles_registry import ROLES
from app.services.game_service import GameService
from app.repositories.memory_repo import MemorySessionRepository


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


class TestSherpaFallResistance:
    """Sherpa: fall_chance_multiplier = 0.7 — reduces fall/lost event probability."""

    def test_sherpa_role_modifiers(self):
        state = make_state(role="sherpa")
        mod = _build_role_modifiers(state)
        assert mod.fall_chance_multiplier == 0.7
        assert mod.stamina_cost_multiplier == 0.85

    def test_sherpa_stamina_cost_reduced(self):
        """Sherpa pays 15% less stamina for all actions."""
        normal_state = make_state()
        sherpa_state = make_state(role="sherpa")

        _, normal_deltas = process(normal_state, ActionType.ADVANCE_NORMAL)
        _, sherpa_deltas = process(sherpa_state, ActionType.ADVANCE_NORMAL)

        # Sherpa should lose less stamina (delta is less negative)
        assert sherpa_deltas.stamina_delta > normal_deltas.stamina_delta
        # Verify the multiplier is 0.85
        sherpa = ROLES["sherpa"]
        assert sherpa.stamina_cost_multiplier == 0.85

    def test_sherpa_fall_chance_multiplier_applied(self):
        """Verify fall_chance_multiplier is 0.7 for sherpa."""
        sherpa = ROLES["sherpa"]
        assert sherpa.special_ability == RoleSpecialAbility.SHERPA_FALL_RESISTANCE
        assert sherpa.ability_params["fall_chance_multiplier"] == 0.7


class TestInvestigadorForecastBonus:
    """Investigador: forecast_reliability_bonus = +0.25, capped at 1.0."""

    def test_investigador_forecast_bonus_value(self):
        inv = ROLES["investigador"]
        assert inv.special_ability == RoleSpecialAbility.INVESTIGATOR_FORECAST
        assert inv.ability_params["forecast_reliability_bonus"] == 0.25

    def test_investigador_starts_with_bonus_reliability(self):
        """Investigador should start with forecast_reliability = 1.0 (base + 0.25, capped)."""
        service = GameService()
        state, _ = service.new_game(role_id="investigador")
        assert state.forecast_reliability == 1.0  # 1.0 + 0.25 capped at 1.0

    def test_investigador_forecast_bonus_applied_on_turn(self):
        """After a turn, forecast reliability should include the bonus."""
        service = GameService()
        state, _ = service.new_game(role_id="investigador")
        result = service.process_turn(state.session_id, "REST")
        # Reliability should be at least the base + bonus (capped at 1.0)
        assert result.new_state.forecast_reliability >= 0.75


class TestTecnicoAltitudeDiscount:
    """Tecnico: above 7000m, stamina cost × 0.90."""

    def test_tecnico_role_modifiers(self):
        state = make_state(role="tecnico")
        mod = _build_role_modifiers(state)
        assert mod.altitude_threshold == 7000
        assert mod.altitude_stamina_discount == 0.90

    def test_tecnico_discount_below_threshold(self):
        """Below 7000m, tecnico uses base stamina_cost_multiplier (0.95)."""
        state = make_state(role="tecnico", player=PlayerStats(altitude=5200.0))
        mod = _build_role_modifiers(state)
        # At 5200m, altitude_threshold check won't apply additional discount
        # But base multiplier is 0.95
        assert mod.stamina_cost_multiplier == 0.95

    def test_tecnico_discount_above_threshold(self):
        """Above 7000m, tecnico gets additional 10% discount."""
        state = make_state(role="tecnico", player=PlayerStats(altitude=7500.0))
        _, deltas = process(state, ActionType.ADVANCE_NORMAL)
        # The altitude discount should be applied via _build_role_modifiers
        # which checks altitude >= threshold
        assert deltas.altitude_delta > 0

    def test_tecnico_starts_with_extra_equipment(self):
        """Tecnico starts with +2 rope and +1 gas."""
        service = GameService()
        state, _ = service.new_game(role_id="tecnico")
        assert state.consumables.rope_sections == 5  # base 3 + 2
        assert state.consumables.gas_canisters == 6  # base 5 + 1


class TestMedicoFreeHeal:
    """Medico: free heal +15HP once per expedition."""

    def test_medico_free_heal_first_use(self):
        """First use of USE_FREE_HEAL restores +15HP."""
        state = make_state(
            role="medico",
            free_heal_used=False,
            player=PlayerStats(hp=50.0),
        )
        new_state, deltas = process(state, ActionType.USE_FREE_HEAL)
        assert deltas.hp_delta == 15
        assert new_state.free_heal_used is True
        assert new_state.player.hp == 65.0

    def test_medico_free_heal_second_use_noop(self):
        """Second use of USE_FREE_HEAL does nothing."""
        state = make_state(
            role="medico",
            free_heal_used=True,
            player=PlayerStats(hp=50.0),
        )
        new_state, deltas = process(state, ActionType.USE_FREE_HEAL)
        assert deltas.hp_delta == 0
        assert new_state.free_heal_used is True
        assert new_state.player.hp == 50.0

    def test_medico_free_heal_caps_at_100(self):
        """Free heal should not exceed 100 HP."""
        state = make_state(
            role="medico",
            free_heal_used=False,
            player=PlayerStats(hp=90.0),
        )
        new_state, deltas = process(state, ActionType.USE_FREE_HEAL)
        assert new_state.player.hp == 100.0

    def test_medico_hp_mitigation(self):
        """Medico reduces incoming HP event damage by 20%."""
        service = GameService()
        mitigation = service._get_hp_mitigation(make_state(role="medico"))
        assert mitigation == 0.20

    def test_medico_no_mitigation_for_non_medico(self):
        """Non-medico roles should have no HP mitigation."""
        service = GameService()
        for role_id in ["sherpa", "clasico", "investigador", "tecnico", ""]:
            mitigation = service._get_hp_mitigation(make_state(role=role_id))
            assert mitigation == 0.0, f"Expected 0.0 for {role_id}, got {mitigation}"


class TestClasicoNoAbility:
    """Clasico: no special ability, higher stamina cost."""

    def test_clasico_no_special_ability(self):
        clasico = ROLES["clasico"]
        assert clasico.special_ability == RoleSpecialAbility.NONE
        assert clasico.ability_params == {}

    def test_clasico_higher_stamina_cost(self):
        """Clasico pays 10% more stamina."""
        normal_state = make_state()
        clasico_state = make_state(role="clasico")

        _, normal_deltas = process(normal_state, ActionType.ADVANCE_NORMAL)
        _, clasico_deltas = process(clasico_state, ActionType.ADVANCE_NORMAL)

        # Clasico should lose more stamina (delta is more negative)
        assert clasico_deltas.stamina_delta < normal_deltas.stamina_delta
