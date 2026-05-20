import random

from app.models.enums import EventType, WeatherState


EVENT_DEFINITIONS = {
    EventType.DISTANT_AVALANCHE: {
        "narrative": [
            "Una avalancha lejana retumba en el valle. El eco atraviesa la cordillera.",
            "El rugido sordo de una avalancha distante reverbera a través del glaciar. Sentís vibrar la roca bajo tus botas.",
            "A lo lejos, una columna de nieve se desploma en la oscuridad. El K2 te recuerda quién manda acá."
        ],
        "willpower_delta": -15,
    },
    EventType.HALLUCINATION: {
        "narrative": [
            "Las sombras danzan en tu visión periférica. La hipoxia te susurra al oído.",
            "Escuchás voces familiares que te llaman por tu nombre desde la ventisca. Pero acá no hay nadie.",
            "El contorno de las rocas se deforma. Creés ver un refugio cálido, pero solo es hielo eterno.",
            "De golpe, sentís que estás escalando junto a alguien más, una presencia silenciosa que imita cada paso."
        ],
        "willpower_delta": -20,
    },
    EventType.WIND_GUST: {
        "narrative": [
            "Una ráfaga violenta te golpea. Pierdes el equilibrio por un instante.",
            "El viento aúlla de golpe y te empuja hacia el abismo. Tenés que aferrarte al hielo.",
            "Una ráfaga helada te azota la cara como un látigo, congelándote el aliento instantáneamente."
        ],
        "stamina_delta": -15,
    },
    EventType.O2_REGULATOR_FAIL: {
        "narrative": [
            "El regulador de oxígeno emite un silbido agudo. El flujo cae a cero.",
            "De repente, no entra aire en la máscara. Mirás el dial: el regulador se congeló por completo.",
            "Un chasquido metálico en tu mochila y el flujo dulce de oxígeno se interrumpe abruptamente."
        ],
        "oxygen_delta": -100,
    },
    EventType.FROSTBITE: {
        "narrative": [
            "El frío muerde tus dedos con insistencia. Ya no los sientes.",
            "Tus extremidades pierden toda sensibilidad. La piel se torna blanca y rígida como el cristal.",
            "Un dolor punzante en los pies da paso a una insensibilidad total. El congelamiento avanza."
        ],
        "hp_delta": -10,
        "temp_delta": -2,
    },
    EventType.PULMONARY_EDEMA: {
        "narrative": [
            "Un líquido espeso llena tus pulmones. Cada respiración es una batalla.",
            "Sentís un gorgoteo constante en el pecho al inhalar. Te ahogás en tu propio cuerpo.",
            "Toses con desesperación, pero el aire simplemente no entra. Tus pulmones se están llenando de fluido."
        ],
        "hp_delta": -20,
        "stamina_delta": -30,
    },
    EventType.TENT_COLLAPSE: {
        "narrative": [
            "La carpa cede bajo el peso de la nieve. Quedás expuesto a la tormenta.",
            "Un crujido seco y la estructura de la carpa colapsa sobre tu cara, sepultándote en lona y nieve.",
            "El viento desgarra la lona del campamento. El frío de la tormenta invade tu único refugio."
        ],
        "stamina_delta": -25,
        "temp_delta": -3,
    },
    EventType.PARTNER_VISION: {
        "narrative": [
            "Creés ver otra figura en la nieve, pero cuando girás no hay nadie.",
            "Una silueta humana te hace señas desde la cresta superior. Parpadeás y desaparece.",
            "A lo lejos, ves a un alpinista descendiendo hacia vos. Cuando te acercás, es solo una roca cubierta de hielo."
        ],
        "willpower_delta": -5,
    },
    EventType.EQUIPMENT_DROP: {
        "narrative": [
            "Algo se desliza hacia abajo en la oscuridad. Una sección de cuerda, quizás.",
            "Sentís un tirón leve en el arnés. Al revisar, una de tus cuerdas fijas se ha perdido en la pendiente.",
            "Un tintineo metálico resuena colina abajo. Parte de tu equipo de seguridad se ha ido para siempre."
        ],
        "rope_delta": -1,
    },
    EventType.SECOND_WIND: {
        "narrative": [
            "Una fuerza inesperada te recorre. El cuerpo responde más allá del agotamiento.",
            "El dolor en las piernas da paso a un calor repentino. La voluntad se impone sobre la fatiga.",
            "Un destello de claridad mental disipa el cansancio. Encontrás fuerzas donde no quedaba nada."
        ],
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


def roll_event(state, last_action: str = "") -> dict | None:
    if not _is_alive(state.status):
        return None

    if not last_action and getattr(state, "last_action", None):
        last_action = state.last_action.value if hasattr(state.last_action, "value") else str(state.last_action)

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
            "narrative": random.choice(data["narrative"]),
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
        "narrative": random.choice(data["narrative"]),
        "hp_delta": data.get("hp_delta", 0),
        "stamina_delta": data.get("stamina_delta", 0),
        "temp_delta": data.get("temp_delta", 0),
        "willpower_delta": data.get("willpower_delta", 0),
        "oxygen_delta": data.get("oxygen_delta", 0),
        "rope_delta": data.get("rope_delta", 0),
    }