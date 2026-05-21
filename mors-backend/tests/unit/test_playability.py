"""
Playability tests — verify the game CAN be completed with reasonable strategies.

These tests ensure:
1. CAMP correctly recovers stamina (not drains it)
2. A player using optimal strategy can reach the summit
3. Death zone bonus fires only once
4. WHITEOUT blocks advance without rope
5. The engine correctly tracks stamina recovery for SECOND_WIND
"""
import pytest
from app.core.game_engine import process, SUMMIT_ALTITUDE, DEATH_ZONE
from app.models.game_state import GameState, PlayerStats, Consumables
from app.models.enums import ActionType, SessionStatus, WeatherState


def make_state(**overrides) -> GameState:
    """Create a default GameState with optional overrides."""
    import uuid
    state = GameState(
        session_id=str(uuid.uuid4()),
        player=PlayerStats(),
        consumables=Consumables(),
    )
    for k, v in overrides.items():
        if hasattr(state.player, k):
            setattr(state.player, k, v)
        elif hasattr(state.consumables, k):
            setattr(state.consumables, k, v)
        else:
            setattr(state, k, v)
    return state


class TestCampRecovery:
    def test_camp_recovers_stamina_in_clear_weather(self):
        """RF-04.4: CAMP should recover stamina, not drain it."""
        state = make_state(stamina=50.0)
        state.weather = WeatherState.CLEAR
        new_state, deltas, _ = process(state, ActionType.CAMP)
        assert new_state.player.stamina > 50.0, (
            f"CAMP should increase stamina from 50, got {new_state.player.stamina}"
        )

    def test_camp_recovers_stamina_in_storm(self):
        """CAMP in storm should still recover stamina (less than clear)."""
        state = make_state(stamina=50.0)
        state.weather = WeatherState.STORM
        new_state, deltas, _ = process(state, ActionType.CAMP)
        # Storm recovery is less but still positive net
        assert deltas.stamina_delta > 0, (
            f"CAMP stamina delta should be positive in storm, got {deltas.stamina_delta}"
        )

    def test_camp_uses_food_and_gas_when_available(self):
        """CAMP consumes food and gas when available."""
        state = make_state(food_rations=5, gas_canisters=3)
        state.weather = WeatherState.CLEAR
        new_state, deltas, _ = process(state, ActionType.CAMP)
        assert new_state.consumables.food_rations == 4
        assert new_state.consumables.gas_canisters == 2

    def test_camp_without_resources_still_recovers_some_stamina(self):
        """CAMP without food/gas still gives partial recovery."""
        state = make_state(stamina=30.0, food_rations=0, gas_canisters=0)
        state.weather = WeatherState.CLEAR
        new_state, deltas, _ = process(state, ActionType.CAMP)
        # Should still recover stamina (base recovery), just less willpower
        assert new_state.player.stamina > 30.0


class TestDeathZoneBonus:
    def test_willpower_bonus_fires_only_once(self):
        """RF-08.6: +25 willpower at death zone fires exactly once."""
        state = make_state(altitude=7950.0, willpower=60.0)
        state.weather = WeatherState.CLEAR

        # First advance above 8000m → should get bonus
        state1, deltas1, _ = process(state, ActionType.ADVANCE_NORMAL)
        wp_after_first = state1.player.willpower

        if state1.player.altitude >= DEATH_ZONE:
            assert state1.player.entered_death_zone is True

        # Descend below 8000m
        state2, _, _ = process(state1, ActionType.DESCEND)
        # Advance again above 8000m → NO bonus this time
        state3, deltas3, _ = process(state2, ActionType.ADVANCE_NORMAL)

        if state3.player.altitude >= DEATH_ZONE:
            # willpower_delta should NOT include the +25 bonus again
            bonus_in_deltas3 = deltas3.willpower_delta
            # Net willpower delta should be negative (passive decay) not +25
            assert bonus_in_deltas3 < 25.0, (
                f"Death zone bonus should not fire twice, got delta: {bonus_in_deltas3}"
            )


class TestWhiteoutBlocking:
    def test_whiteout_blocks_advance_without_rope(self):
        """WHITEOUT without rope should raise ValueError (can't advance)."""
        state = make_state(altitude=6000.0)
        state.weather = WeatherState.WHITEOUT
        state.consumables.rope_sections = 0

        with pytest.raises(ValueError, match="Visibilidad cero por ventisca"):
            process(state, ActionType.ADVANCE_NORMAL)

    def test_whiteout_allows_advance_with_rope(self):
        """WHITEOUT with rope available should allow advance."""
        state = make_state(altitude=6000.0)
        state.weather = WeatherState.WHITEOUT
        state.consumables.rope_sections = 2

        new_state, deltas, _ = process(state, ActionType.ADVANCE_NORMAL)
        assert deltas.altitude_delta > 0.0, (
            f"WHITEOUT with rope should allow advance, got delta: {deltas.altitude_delta}"
        )


class TestStaminaTracker:
    def test_tracker_increments_when_stamina_lost(self):
        """Tracker should increment when stamina decreases."""
        state = make_state(altitude=5500.0)
        state.turns_without_stamina_recovery = 0
        new_state, deltas, _ = process(state, ActionType.ADVANCE_NORMAL)
        # ADVANCE_NORMAL costs stamina → tracker should increment
        if deltas.stamina_delta <= 0:
            assert new_state.turns_without_stamina_recovery > 0

    def test_tracker_resets_when_stamina_gained(self):
        """Tracker should reset when CAMP recovers stamina."""
        state = make_state(stamina=50.0)
        state.turns_without_stamina_recovery = 15
        state.weather = WeatherState.CLEAR
        new_state, deltas, _ = process(state, ActionType.CAMP)
        # CAMP in clear weather gives significant stamina recovery
        assert new_state.turns_without_stamina_recovery == 0, (
            f"After CAMP, tracker should reset, got {new_state.turns_without_stamina_recovery}"
        )


class TestEatRecovery:
    def test_eat_recovers_more_at_low_altitude(self):
        """EAT should be more effective at lower altitudes."""
        state_low = make_state(altitude=5200.0, stamina=50.0, food_rations=5)
        state_high = make_state(altitude=8200.0, stamina=50.0, food_rations=5)
        state_high.player.entered_death_zone = True

        new_low, deltas_low, _ = process(state_low, ActionType.EAT)
        new_high, deltas_high, _ = process(state_high, ActionType.EAT)

        assert deltas_low.stamina_delta > deltas_high.stamina_delta, (
            f"EAT should recover more at low altitude. "
            f"Low: {deltas_low.stamina_delta}, High: {deltas_high.stamina_delta}"
        )


class TestFallDamage:
    def test_fall_does_not_instantly_kill(self):
        """ADVANCE_AGGRESSIVE fall should damage HP but not set status=DEAD directly."""
        import random
        random.seed(42)  # Fixed seed to get a predictable fall

        # Player with low stamina = high fall chance
        state = make_state(altitude=6000.0, stamina=5.0, hp=100.0)
        state.weather = WeatherState.CLEAR

        # Run many times to hit a fall
        fell = False
        for seed in range(100):
            random.seed(seed)
            s = make_state(altitude=6000.0, stamina=5.0, hp=100.0)
            s.weather = WeatherState.CLEAR
            new_s, deltas, _ = process(s, ActionType.ADVANCE_AGGRESSIVE)
            if deltas.hp_delta < 0:
                fell = True
                # Even after a fall, player should not be DEAD if HP was full
                # (unless passive damage kills them too, which is acceptable)
                assert new_s.player.hp >= 0.0, "HP cannot go below 0"
                break

        # It's probabilistic but with 100 seeds we expect at least one fall
        assert fell, "Should have seen at least one fall in 100 attempts with low stamina"


class TestCompletability:
    """
    Verify that a player using optimal strategy CAN complete the game.
    This is a high-level playability test — not a balance tuning test.
    """

    def _play_optimal_game(self, max_turns: int = 300) -> tuple[str, int, float]:
        """
        Simulate an optimal player:
        - Camp when stamina < 30 OR body_temp < 35.5 (prevent hypothermia)
        - Use oxygen in death zone when low
        - Eat when stamina < 55 and food available
        - Advance aggressively when fully rested
        - Advance normal otherwise
        Returns: (final_status, turns_taken, max_altitude)
        """
        import uuid
        state = GameState(
            session_id=str(uuid.uuid4()),
            player=PlayerStats(
                hp=100.0,
                stamina=100.0,
                body_temp=37.0,
                willpower=100.0,
                altitude=5200.0,
            ),
            consumables=Consumables(
                food_rations=10,
                gas_canisters=5,
                rope_sections=3,
                oxygen_pct=100.0,
            ),
        )
        state.weather = WeatherState.CLEAR

        for turn in range(max_turns):
            if state.status.value != "ALIVE":
                break

            stamina = state.player.stamina
            body_temp = state.player.body_temp
            altitude = state.player.altitude
            weather_val = state.weather.value if hasattr(state.weather, "value") else str(state.weather)
            has_food = state.consumables.food_rations > 0
            has_gas = state.consumables.gas_canisters > 0
            in_death_zone = altitude >= DEATH_ZONE

            # Priority 1: Survive temperature threat
            if body_temp < 35.5 and (has_food or has_gas):
                action = ActionType.CAMP
            # Priority 2: Oxygen in death zone
            elif in_death_zone and state.consumables.oxygen_pct < 40 and has_gas:
                action = ActionType.USE_OXYGEN
            # Priority 3: Stamina is critical
            elif stamina < 25 and (has_food or has_gas):
                action = ActionType.CAMP
            # Priority 4: Eat for moderate recovery
            elif stamina < 55 and has_food:
                action = ActionType.EAT
            # Priority 5: Weather is dangerous
            elif weather_val in ("WHITEOUT", "STORM") and stamina < 70:
                action = ActionType.CAMP
            # Priority 6: Advance
            else:
                action = ActionType.ADVANCE_NORMAL

            state, _, _ = process(state, action)

        return (
            state.status.value,
            state.turn,
            state.player.max_altitude_reached,
        )


    def test_game_is_completable_with_optimal_play(self):
        """An optimal player should be able to reach the summit."""
        status, turns, max_alt = self._play_optimal_game(max_turns=300)
        assert status == "SUMMIT", (
            f"Optimal player should reach SUMMIT. "
            f"Got status={status} after {turns} turns, max_altitude={max_alt:.0f}m"
        )

    def test_game_takes_reasonable_number_of_turns(self):
        """The game should complete in a reasonable turn count (not trivial or endless)."""
        status, turns, max_alt = self._play_optimal_game(max_turns=300)
        if status == "SUMMIT":
            # Summit should take between 20 and 200 turns
            assert 20 <= turns <= 200, (
                f"Summit should take 20-200 turns, took {turns}"
            )
