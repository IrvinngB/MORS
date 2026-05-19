from app.models.enums import EventType


EVENT_DEFINITIONS = {
    EventType.DISTANT_AVALANCHE: {
        "narrative": "Una avalancha lejana retumba en el valle. El eco atraviesa la cordillera.",
        "willpower_delta": -15,
    },
    EventType.HALLUCINATION: {
        "narrative": "Las sombras danzan en tu visión peripheral. La hipoxia te susurra al oído.",
        "willpower_delta": -20,
    },
    EventType.WIND_GUST: {
        "narrative": "Una ráfaga violenta te golpea. Pierdes el equilibrio por un instante.",
        "stamina_delta": -15,
    },
    EventType.O2_REGULATOR_FAIL: {
        "narrative": "El regulador de oxígeno emite un silbido agudo. Algo no va bien.",
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
        "narrative": "La carpa cede bajo el peso de la nieve. Quedas expuesto a la tormenta.",
        "stamina_delta": -25,
        "temp_delta": -3,
    },
    EventType.PARTNER_VISION: {
        "narrative": "Crees ver otra figura en la nieve, pero cuando giras no hay nadie.",
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
    return min(base, 0.50)


def _can_second_wind(state) -> bool:
    return state.turns_without_stamina_recovery >= 10


def _is_alive(status) -> bool:
    val = status.value if hasattr(status, "value") else status
    return val == "ALIVE"


def roll_event(state) -> dict | None:
    import random

    if not _is_alive(state.status):
        return None

    if random.random() > _base_event_chance(state):
        return None

    if random.random() < 0.1 and _can_second_wind(state):
        event_type = EventType.SECOND_WIND
        data = EVENT_DEFINITIONS[event_type]
        return {
            "event_type": event_type.value,
            "narrative": data["narrative"],
            "stamina_delta": data.get("stamina_delta", 0),
            "willpower_delta": data.get("willpower_delta", 0),
        }

    critical_events = [
        EventType.HALLUCINATION,
        EventType.PULMONARY_EDEMA,
        EventType.FROSTBITE,
    ]
    if state.player.turns_above_8000 > 0:
        weights = [0.3, 0.4, 0.3]
        event_type = random.choices(critical_events, weights=weights, k=1)[0]
    else:
        non_critical = [
            EventType.DISTANT_AVALANCHE,
            EventType.WIND_GUST,
            EventType.O2_REGULATOR_FAIL,
            EventType.TENT_COLLAPSE,
            EventType.PARTNER_VISION,
            EventType.EQUIPMENT_DROP,
        ]
        weights = [0.15] * len(non_critical)
        event_type = random.choices(non_critical, weights=weights, k=1)[0]

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