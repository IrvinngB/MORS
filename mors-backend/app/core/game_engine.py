import random
from datetime import datetime, timezone

from app.models.enums import (
    ActionType,
    DeathCause,
    SessionStatus,
    WeatherState,
    WEATHER_MODIFIERS,
)
from app.models.game_state import Consumables, GameState, PlayerStats, TurnDeltas


SUMMIT_ALTITUDE = 8611.0
DEATH_ZONE = 8000.0
STARTING_ALTITUDE = 5200.0
BASE_STAMINA_COST = 12.0  # Reduced from 15 → more forgiving base cost
AGGRESSIVE_ALTITUDE_GAIN = 280.0
NORMAL_ALTITUDE_GAIN = 150.0
DESCENT_ALTITUDE = 200.0


def _oxygen_mod(oxygen_pct: float) -> float:
    if oxygen_pct > 50:
        return 0.8
    elif oxygen_pct < 30:
        return 1.4
    return 1.0


def _willpower_penalty(willpower: float) -> float:
    if willpower < 20:
        return 1.15
    return 1.0


def _stamina_cost(
    altitude: float,
    weather: WeatherState,
    oxygen_pct: float,
    willpower: float,
) -> float:
    altitude_factor = 1 + (altitude / 8000) ** 2
    weather_mod = WEATHER_MODIFIERS[weather]
    ox_mod = _oxygen_mod(oxygen_pct)
    wp_mod = _willpower_penalty(willpower)
    return BASE_STAMINA_COST * altitude_factor * weather_mod * ox_mod * wp_mod


def _night_penalty(is_night: bool) -> float:
    return 1.3 if is_night else 1.0


def _body_temp_delta(
    altitude: float,
    weather: WeatherState,
    is_night: bool,
    route_secured: int,
) -> float:
    # Reduced base drop: 0.05°C/turn (was 0.1) — a well-equipped climber manages cold
    base_drop = 0.05
    altitude_factor = (altitude - STARTING_ALTITUDE) / 1000.0
    weather_factor = WEATHER_MODIFIERS[weather] - 1.0
    night_factor = 0.15 if is_night else 0.0  # Night is harsher but not extreme
    secured_reduction = min(0.08, route_secured * 0.015)

    delta = -(base_drop + altitude_factor * 0.03 + weather_factor * 0.08 + night_factor - secured_reduction)
    return max(delta, -4.0)


def _willpower_delta(
    altitude: float,
    turn: int,
    turns_above_8000: int,
    is_night: bool,
    weather: WeatherState,
) -> float:
    base = 0.5
    altitude_factor = (altitude - STARTING_ALTITUDE) / 1000.0
    night_factor = 0.3 if is_night else 0.0
    death_zone_factor = turns_above_8000 * 0.15

    delta = -(base + altitude_factor * 0.1 + night_factor + death_zone_factor)
    if weather == WeatherState.WHITEOUT:
        delta -= 1.0
    return max(delta, -15.0)


def _camp_stamina_recovery(weather: WeatherState, is_night: bool) -> float:
    """CAMP recovers stamina. Amount depends on conditions."""
    base_recovery = 30.0
    if weather == WeatherState.CLEAR:
        base_recovery = 40.0
    elif weather in (WeatherState.STORM, WeatherState.WHITEOUT):
        base_recovery = 15.0
    if is_night:
        base_recovery *= 0.85
    return base_recovery


def _camp_temp_recovery(has_gas: bool, weather: WeatherState) -> float:
    """CAMP temperature recovery. Gas heats the tent, making a significant difference."""
    base = 3.0
    if has_gas:
        base += 2.0  # Gas canisters provide meaningful heating
    if weather in (WeatherState.STORM, WeatherState.WHITEOUT):
        base -= 1.0  # Storm reduces heating effectiveness
    return max(base, 1.0)


def _eat_stamina_recovery(altitude: float) -> float:
    """EAT recovery scales down at altitude (body absorbs less at high altitude)."""
    if altitude >= DEATH_ZONE:
        return 10.0
    elif altitude >= 7000:
        return 15.0
    return 20.0


def _process_action(
    state: GameState,
    action: ActionType,
    is_night: bool,
) -> tuple[GameState, TurnDeltas]:
    new_state = state.model_copy(deep=True)
    deltas = TurnDeltas()
    new_state.turn += 1

    weather = WeatherState(state.weather) if isinstance(state.weather, str) else state.weather
    weather_mod = WEATHER_MODIFIERS[weather]
    stamina_cost = _stamina_cost(
        new_state.player.altitude,
        weather,
        new_state.consumables.oxygen_pct,
        new_state.player.willpower,
    )
    night_mult = _night_penalty(is_night)

    match action:
        case ActionType.ADVANCE_NORMAL:
            # WHITEOUT without rope blocks advance
            if weather == WeatherState.WHITEOUT and new_state.consumables.rope_sections == 0:
                # Cannot advance — treat as REST with morale penalty
                deltas.stamina_delta = 5.0
                deltas.willpower_delta = -5.0
            else:
                altitude_gain = NORMAL_ALTITUDE_GAIN
                cost = stamina_cost * 1.0 * night_mult
                deltas.altitude_delta = altitude_gain
                deltas.stamina_delta = -cost

        case ActionType.ADVANCE_AGGRESSIVE:
            # WHITEOUT without rope blocks advance
            if weather == WeatherState.WHITEOUT and new_state.consumables.rope_sections == 0:
                deltas.stamina_delta = 5.0
                deltas.willpower_delta = -8.0
            else:
                altitude_gain = AGGRESSIVE_ALTITUDE_GAIN
                cost = stamina_cost * 1.8 * night_mult
                deltas.altitude_delta = altitude_gain
                deltas.stamina_delta = -cost

                fall_chance = 0.05 + max(0, (100 - new_state.player.stamina) / 100 * 0.3) * weather_mod
                fall_chance *= (1 - min(0.3, new_state.route_secured * 0.1))
                if random.random() < fall_chance:
                    # Fall causes damage but does NOT directly kill — let passive damage handle death
                    fall_damage = 20.0 + random.uniform(0, 15.0)
                    deltas.hp_delta = -fall_damage
                    new_state.death_cause = DeathCause.DEAD_FALL

        case ActionType.SECURE_ROUTE:
            if new_state.consumables.rope_sections > 0:
                new_state.consumables.rope_sections -= 1
                new_state.route_secured += 3
                deltas.route_secured_delta = 3
                deltas.stamina_delta = -stamina_cost * 0.6
            else:
                # No rope: still takes effort with no benefit
                deltas.stamina_delta = -stamina_cost * 0.3

        case ActionType.CAMP:
            # CAMP recovers stamina (RF-04.4) — does NOT cost stamina
            recovery = _camp_stamina_recovery(weather, is_night)
            deltas.stamina_delta = recovery

            has_gas_for_camp = new_state.consumables.gas_canisters > 0
            if new_state.consumables.food_rations > 0:
                new_state.consumables.food_rations -= 1
                deltas.willpower_delta = 8.0
            else:
                deltas.willpower_delta = 2.0  # Rest still helps willpower even without food

            if has_gas_for_camp:
                new_state.consumables.gas_canisters -= 1

            # Temperature recovery: gas provides meaningful heating
            deltas.temp_delta = _camp_temp_recovery(has_gas_for_camp, weather)


        case ActionType.USE_OXYGEN:
            if new_state.consumables.gas_canisters > 0:
                new_state.consumables.gas_canisters -= 1
                new_state.consumables.oxygen_pct = min(100.0, new_state.consumables.oxygen_pct + 30.0)
                deltas.oxygen_delta = 30.0
                deltas.willpower_delta = 10.0
            else:
                deltas.oxygen_delta = 0.0

        case ActionType.EAT:
            if new_state.consumables.food_rations > 0:
                new_state.consumables.food_rations -= 1
                recovery = _eat_stamina_recovery(new_state.player.altitude)
                deltas.stamina_delta = recovery
                deltas.willpower_delta = 5.0
            # No food: no effect, no error

        case ActionType.DESCEND:
            altitude_loss = DESCENT_ALTITUDE
            cost = stamina_cost * 0.3
            deltas.altitude_delta = -altitude_loss
            deltas.stamina_delta = -cost
            deltas.temp_delta = 0.5
            deltas.willpower_delta = -2.0

        case ActionType.REST:
            deltas.stamina_delta = 10.0
            deltas.temp_delta = 0.3
            deltas.willpower_delta = -3.0

    # Apply stamina delta and clamp
    new_state.player.stamina = max(0.0, min(100.0, new_state.player.stamina + deltas.stamina_delta))

    # Apply HP delta from action (fall damage etc)
    if deltas.hp_delta != 0:
        new_state.player.hp = max(0.0, min(100.0, new_state.player.hp + deltas.hp_delta))

    new_state.player.altitude = max(0.0, new_state.player.altitude + deltas.altitude_delta)

    if new_state.player.altitude > new_state.player.max_altitude_reached:
        new_state.player.max_altitude_reached = new_state.player.altitude

    if new_state.player.altitude >= SUMMIT_ALTITUDE and new_state.player.hp > 0:
        new_state.status = SessionStatus.SUMMIT

    # Death zone: +25 willpower bonus ONLY on first entry
    if new_state.player.altitude >= DEATH_ZONE:
        if not new_state.player.entered_death_zone:
            deltas.willpower_delta += 25.0
            new_state.player.willpower = min(100.0, new_state.player.willpower + 25.0)
            new_state.player.entered_death_zone = True
        new_state.player.turns_above_8000 += 1

    return new_state, deltas


def _apply_passive_damage(state: GameState, deltas: TurnDeltas) -> None:
    """Apply damage from environmental and physiological effects."""
    # Hypothermia: below 35°C → HP loss proportional to temperature deficit
    if state.player.body_temp < 35.0:
        hp_loss = (35.0 - state.player.body_temp) * 2.0
        state.player.hp = max(0.0, state.player.hp - hp_loss)
        deltas.hp_delta -= hp_loss
        if state.player.hp <= 0 and state.death_cause is None:
            state.death_cause = DeathCause.DEAD_COLD

    # Exhaustion: zero stamina → HP loss per turn
    if state.player.stamina <= 0:
        hp_loss = 5.0
        state.player.hp = max(0.0, state.player.hp - hp_loss)
        deltas.hp_delta -= hp_loss
        if state.player.hp <= 0 and state.death_cause is None:
            state.death_cause = DeathCause.DEAD_EXHAUSTION

    # Willpower collapse: doubles HP loss rate from exhaustion
    if state.player.willpower <= 0 and state.player.stamina <= 0:
        hp_loss = 2.5
        state.player.hp = max(0.0, state.player.hp - hp_loss)
        deltas.hp_delta -= hp_loss

    # Fallback death cause
    if state.player.hp <= 0 and state.death_cause is None:
        state.death_cause = DeathCause.DEAD_EXHAUSTION


def _tick(state: GameState, deltas: TurnDeltas, is_night: bool) -> None:
    """Apply all passive per-turn effects."""
    weather = WeatherState(state.weather) if isinstance(state.weather, str) else state.weather

    # Body temperature passive decay
    temp_delta = _body_temp_delta(
        state.player.altitude,
        weather,
        is_night,
        state.route_secured,
    )
    state.player.body_temp += temp_delta
    deltas.temp_delta += temp_delta

    # Willpower passive decay
    wp_delta = _willpower_delta(
        state.player.altitude,
        state.turn,
        state.player.turns_above_8000,
        is_night,
        weather,
    )
    state.player.willpower = max(0.0, min(100.0, state.player.willpower + wp_delta))
    deltas.willpower_delta += wp_delta

    # Oxygen passive drain in death zone
    if state.player.altitude >= DEATH_ZONE:
        o2_drain = 5.0
        old_o2 = state.consumables.oxygen_pct
        state.consumables.oxygen_pct = max(0.0, state.consumables.oxygen_pct - o2_drain)
        actual_drain = old_o2 - state.consumables.oxygen_pct
        deltas.oxygen_delta -= actual_drain

    # Clamp values
    state.player.body_temp = max(0.0, min(45.0, state.player.body_temp))
    state.player.willpower = max(0.0, min(100.0, state.player.willpower))

    _apply_passive_damage(state, deltas)

    # Track consecutive turns without stamina recovery (for SECOND_WIND)
    if deltas.stamina_delta <= 0:
        state.turns_without_stamina_recovery += 1
    else:
        state.turns_without_stamina_recovery = 0

    # Route secured degrades each turn
    if state.route_secured > 0:
        state.route_secured = max(0, state.route_secured - 1)


def process(state: GameState, action: ActionType) -> tuple[GameState, TurnDeltas]:
    is_night = state.turn % 24 >= 12

    new_state, deltas = _process_action(state, action, is_night)

    _tick(new_state, deltas, is_night)

    if new_state.player.hp <= 0 and new_state.status == SessionStatus.ALIVE:
        new_state.status = SessionStatus.DEAD

    new_state.updated_at = datetime.now(timezone.utc)

    return new_state, deltas