from app.core.config import settings


NARRATIVE_TEMPLATES = {
    "intro": [
        "La niebla del valle se mezcla con el silencio. El K2 aguarda, inmutable.",
        "El viento arrastra los últimos vestigios de la planicie. La montaña te llama.",
    ],
    "advance_normal": [
        "Avanzas con paso firme. El terreno cede bajo tus botas.",
        "La ascensión continúa. Cada paso es una negociación con la altura.",
    ],
    "advance_aggressive": [
        "Te lanzas hacia arriba con determinación. El aire se vuelve más escaso.",
        "La pendiente se acentúa. Tus músculos protestan pero el cuerpo responde.",
    ],
    "secure_route": [
        "Clavas una estaca en la roca helada. La ruta queda marcada.",
        "Aseguras un tramo. El siguiente paso estará protegido.",
    ],
    "camp": [
        "Armas el campamento entre temblores. El suelo congelado complica todo.",
        "La tienda resiste. Te permites un respiro mientras la tormenta pasa.",
    ],
    "use_oxygen": [
        "Abre el tanque. El oxígeno fluye y el mundo se vuelve más claro.",
        "Respiras profundamente. La niebla en tu mente se disipa.",
    ],
    "eat": [
        "Una ración tibia. El cuerpo agradece el gesto.",
        "Comes lo mínimo. La supervivencia no permite excesos.",
    ],
    "descend": [
        "Desciendes. La presión en tu pecho disminuye con cada metro.",
        "Bajas el ritmo. El valle te recibe con algo de calor residual.",
    ],
    "rest": [
        "Te detienes. Solo un momento, pero el cuerpo lo necesitaba.",
        "Esperas. La inmovilidad pesa, pero el descanso es necesario.",
    ],
    "low_willpower": [
        "La mente vagabundea. El suelo parece más cercano de lo que debería.",
        "La voluntad se erosiona. Cada paso es una duda.",
    ],
    "death_zone": [
        "La zona de la muerte no perdona. El cuerpo consume sus propias reservas.",
        "Pasas los 8000 metros. El oxígeno es un lujo y el tiempo se agota.",
    ],
    "storm": [
        "La tormenta te envuelve. Visibility cero.",
        "El viento aúlla. La nieve golpea tu rostro sin piedad.",
    ],
}


def _select_template(key: str, willpower: float) -> str:
    templates = NARRATIVE_TEMPLATES.get(key, NARRATIVE_TEMPLATES["advance_normal"])
    if willpower < 30 and key not in ("low_willpower", "death_zone"):
        alt_templates = NARRATIVE_TEMPLATES["low_willpower"]
        return alt_templates[hash(str(willpower)) % len(alt_templates)]
    return templates[hash(str(willpower)) % len(templates)]


def generate_narrative(
    action: str,
    deltas: dict,
    event: dict | None,
    willpower: float,
    altitude: float,
    weather: str,
) -> str:
    import random

    if event:
        return event.get("narrative", _select_template(action, willpower))

    template_key = action
    if willpower < 30:
        template_key = "low_willpower"
    elif altitude >= 8000:
        template_key = "death_zone"
    elif weather in ("STORM", "WHITEOUT"):
        template_key = "storm"

    narrative = _select_template(template_key, willpower)

    delta_parts = []
    if deltas.get("stamina_delta", 0) < -20:
        delta_parts.append("El agotamiento se acumula.")
    if deltas.get("temp_delta", 0) < -2:
        delta_parts.append("El frío penetra hasta los huesos.")
    if deltas.get("willpower_delta", 0) < -10:
        delta_parts.append("La mente se nubla.")

    if delta_parts:
        narrative += " " + " ".join(delta_parts)

    if random.random() < 0.3:
        suffixes = [
            "El K2 no perdona.",
            "La montaña exige.",
            "Cada turno cuenta.",
            "El tiempo corre contra ti.",
        ]
        narrative += " " + random.choice(suffixes)

    return narrative


def generate_epitaph(
    death_cause: str,
    max_altitude: float,
    turn: int,
    worst_moment: str,
) -> str:
    import random

    epitaphs = [
        "Non Omnis Moriar — No todo de mí morirá en esta montaña.",
        "El K2 me ha reclamado, pero no me ha vencido.",
        "La altura me llamó y yo respondí.",
        "Mi nombre se perderá en la nieve, pero la escalada fue real.",
    ]

    cause_map = {
        "DEAD_EXHAUSTION": "agotamiento",
        "DEAD_COLD": "congelamiento",
        "DEAD_FALL": "caída",
        "DEAD_STORM": "tormenta",
        "DEAD_EDEMA": "edema pulmonar",
    }

    cause_text = cause_map.get(death_cause, "causas desconocidas")
    base = random.choice(epitaphs)
    return f"{base} Altitud máxima: {max_altitude:.0f}m. Causa de muerte: {cause_text}. Turno: {turn}."