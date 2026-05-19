import random

from app.models.enums import EventType, WeatherState


EVENT_DEFINITIONS = {
    EventType.DISTANT_AVALANCHE: {
        "narrative": "Una avalancha lejana retumba en el valle. El eco atraviesa la cordillera.",
        "willpower_delta": -15,
    },
    EventType.HALLUCINATION: {
        "narrative": "Las sombras danzan en tu visión periférica. La hipoxia te susurra al oído.",
        "willpower_delta": -20,
    },
    EventType.WIND_GUST: {
        "narrative": "Una ráfaga violenta te golpea. Pierdes el equilibrio por un instante.",
        "stamina_delta": -15,
    },
    EventType.O2_REGULATOR_FAIL: {
        "narrative": "El regulador de oxígeno emite un silbido agudo. El flujo cae a cero.",
        "oxygen_delta": -100,
    },
    EventType.FROSTBITE: {
        "narrative": "El frío muerde tus dedos con insistencia. Ya no los sientes.",
        "hp_delta": -10,
        "temp_delta": -2,
    },
    EventType.PULMONARY_EDEMA: {
        "narrative": "Un líquido espeso llena tus pulmones. Cada respiración es una batalla.",
        "hp_delta": -20,
        "stamina_delta": -30,
    },
    EventType.TENT_COLLAPSE: {
        "narrative": "La carpa cede bajo el peso de la nieve. Quedás expuesto a la tormenta.",
        "stamina_delta": -25,
        "temp_delta": -3,
    },
    EventType.PARTNER_VISION: {
        "narrative": "Creés ver otra figura en la nieve, pero cuando girás no hay nadie.",
        "willpower_delta": -5,
    },
    EventType.EQUIPMENT_DROP: {
        "narrative": "Algo se desliza hacia abajo en la oscuridad. Una sección de cuerda, quizás.",
        "rope_delta": -1,
    },
    EventType.SECOND_WIND: {
        "narrative": "Una fuerza inesperada te recorre. El cuerpo responde más allá del agotamiento.",
        "stamina_delta": 20,
        "willpower_delta": 10,
    },
}


def _base_event_chance(state) -> float:
    base = 0.15
    if state.player.turns_above_8000 > 0:
        base += state.player.turns_above_8000 * 0.05
    # Low willpower increases event chance
    if state.player.willpower < 30:
        base += 0.05
    return min(base, 0.50)


def _can_second_wind(state) -> bool:
    return state.turns_without_stamina_recovery >= 10


def _is_alive(status) -> bool:
    val = status.value if hasattr(status, "value") else status
    return val == "ALIVE"


def _get_weather(state) -> str:
    w = state.weather
    return w.value if hasattr(w, "value") else str(w)


def _get_last_action(state) -> str:
    """Infer last action from context — used for contextual event filtering."""
    # We don't store last_action in state, so we use heuristics
    return getattr(state, "_last_action", "")


def roll_event(state, last_action: str = "") -> dict | None:
    if not _is_alive(state.status):
        return None

    if random.random() > _base_event_chance(state):
        return None

    weather = _get_weather(state)
    in_death_zone = state.player.turns_above_8000 > 0

    # SECOND_WIND: only if exhausted for 10+ turns without recovery
    if random.random() < 0.1 and _can_second_wind(state):
        event_type = EventType.SECOND_WIND
        data = EVENT_DEFINITIONS[event_type]
        return {
            "event_type": event_type.value,
            "narrative": data["narrative"],
            "stamina_delta": data.get("stamina_delta", 0),
            "willpower_delta": data.get("willpower_delta", 0),
        }

    # Build contextual event pool
    if in_death_zone:
        # Death zone: heavy critical events
        event_pool = [
            EventType.HALLUCINATION,
            EventType.PULMONARY_EDEMA,
            EventType.FROSTBITE,
        ]
        weights = [0.3, 0.4, 0.3]
    else:
        # Below death zone: lighter events
        event_pool = []
        weights = []

        # Always possible
        event_pool.append(EventType.DISTANT_AVALANCHE)
        weights.append(0.20)

        event_pool.append(EventType.PARTNER_VISION)
        weights.append(0.15)

        event_pool.append(EventType.EQUIPMENT_DROP)
        weights.append(0.15)

        # Only if windy/storm conditions
        if weather in ("WIND", "STORM", "WHITEOUT"):
            event_pool.append(EventType.WIND_GUST)
            weights.append(0.25)
            # TENT_COLLAPSE only makes sense during CAMP action in a storm
            if last_action == "CAMP":
                event_pool.append(EventType.TENT_COLLAPSE)
                weights.append(0.20)

        # O2_REGULATOR_FAIL only if player has oxygen
        if state.consumables.oxygen_pct > 0:
            event_pool.append(EventType.O2_REGULATOR_FAIL)
            weights.append(0.15)

        # Hallucination possible at high altitude even below death zone
        if state.player.altitude >= 7000:
            event_pool.append(EventType.HALLUCINATION)
            weights.append(0.10)

        # FROSTBITE more likely when cold
        if state.player.body_temp < 35.5:
            event_pool.append(EventType.FROSTBITE)
            weights.append(0.20)

    if not event_pool:
        return None

    # Normalize weights
    total = sum(weights)
    norm_weights = [w / total for w in weights]

    event_type = random.choices(event_pool, weights=norm_weights, k=1)[0]
    data = EVENT_DEFINITIONS[event_type]

    return {
        "event_type": event_type.value,
        "narrative": data["narrative"],
        "hp_delta": data.get("hp_delta", 0),
        "stamina_delta": data.get("stamina_delta", 0),
        "temp_delta": data.get("temp_delta", 0),
        "willpower_delta": data.get("willpower_delta", 0),
        "oxygen_delta": data.get("oxygen_delta", 0),
        "rope_delta": data.get("rope_delta", 0),
    }