import random
from app.core.config import settings


# ── Introducción ────────────────────────────────────────────────
INTRO_TEMPLATES = [
    "La niebla del valle se mezcla con el silencio. El K2 aguarda, inmutable.",
    "El viento arrastra los últimos vestigios de la planicie. La montaña te llama.",
    "A tus pies, el mundo se reduce a hielo y voluntad. La cima es una promesa lejana.",
    "El aire es delgado, el silencio, absoluto. Cada respiración es un acto de fe.",
    "La montaña no te ve. No le importas. Y sin embargo, aquí estás.",
]

# ── Avanzar Normal ──────────────────────────────────────────────
ADVANCE_NORMAL = {
    "low": [
        "Avanzas con paso firme. El terreno cede bajo tus botas.",
        "La ascensión continúa. Cada paso es una negociación con la altura.",
        "El crampon muerde el hielo. Un metro más, siempre un metro más.",
        "Tu respiración marca el ritmo. Inhala, pisa, exhala, repite.",
    ],
    "mid": [
        "El aire se adelgaza. Cada paso requiere más conciencia que fuerza.",
        "La pendiente no perdona. Avanzas con la precisión de quien sabe que un error cuesta caro.",
        "El viento silba entre las rocas. No te detienes.",
    ],
    "high": [
        "Cada paso es una batalla contra tu propio cuerpo. La altitud cobra su tributo.",
        "El oxígeno es un recuerdo. Avanzas por inercia y terquedad.",
        "La montaña se siente más cerca, pero tu cuerpo grita que pare.",
    ],
    "death_zone": [
        "La zona de la muerte no perdona. Cada paso es un acto de rebeldía contra la fisiología.",
        "Tu cuerpo se consume. Avanzas porque detenerte significa morir.",
        "El aire es veneno. Cada respiración quema. Pero la cima está ahí.",
    ],
}

# ── Avanzar Agresivo ────────────────────────────────────────────
ADVANCE_AGGRESSIVE = {
    "low": [
        "Te lanzas hacia arriba con determinación. El aire se vuelve más escaso.",
        "La pendiente se acentúa. Tus músculos protestan pero el cuerpo responde.",
        "Aceleras el paso. La montaña parece retroceder ante tu empuje.",
    ],
    "mid": [
        "Forzas el ritmo. El hielo cruje bajo tus pies. Es una apuesta peligrosa.",
        "La adrenalina te empuja hacia arriba. Pero el cuerpo tiene límites.",
        "Cada movimiento es más arriesgado. La fatiga nubla el juicio.",
    ],
    "high": [
        "Te lanzas hacia lo imposible. El cuerpo grita, la mente ordena avanzar.",
        "Es una locura. Lo sabes. Pero detenerte duele más.",
        "La pendiente se vuelve vertical. Cada paso es un acto de fe ciega.",
    ],
    "death_zone": [
        "Te arrastras hacia arriba con una furia que no sabías que tenías. La muerte te pisa los talones.",
        "Cada movimiento podría ser el último. Avanzas igual.",
        "La zona de la muerte no distingue entre valientes y necios. Tú eres ambos.",
    ],
}

# ── Asegurar Ruta ───────────────────────────────────────────────
SECURE_ROUTE = [
    "Clavas una estaca en la roca helada. La ruta queda marcada para el retorno.",
    "Aseguras un tramo. El siguiente paso estará protegido.",
    "La cuerda tensa contra el viento. Un hilo de seguridad en medio del abismo.",
    "Cada nudo es una promesa: volverás por aquí.",
    "El hielo cede ante el piolet. Aseguras el camino para quien venga después.",
]

# ── Acampar ─────────────────────────────────────────────────────
CAMP = {
    "clear": [
        "Armas el campamento bajo un cielo despejado. Las estrellas parecen más cercanas aquí.",
        "La tienda resiste el viento. Te permites un respiro mientras la noche pasa.",
    ],
    "storm": [
        "La tormenta azota la tienda. Cada ráfaga es un recordatorio de tu fragilidad.",
        "El viento amenaza con arrancar la carpa. Te aferras a la lona como a tu vida.",
        "La nieve se acumula contra la tela. El mundo exterior ha desaparecido.",
    ],
    "default": [
        "Armas el campamento entre temblores. El suelo congelado complica todo.",
        "La tienda es tu único refugio contra la inmensidad helada.",
        "Te refugias. El frío se cuela por las costuras, pero estás vivo.",
    ],
}

# ── Usar Oxígeno ────────────────────────────────────────────────
USE_OXYGEN = [
    "Abres el tanque. El oxígeno fluye y el mundo se vuelve más claro.",
    "Respiras profundamente. La niebla en tu mente se disipa.",
    "El gas silba al salir. Por un momento, recuerdas cómo se siente respirar sin esfuerzo.",
    "La máscara se empaña. Pero el aire que entra es dulce, casi olvidado.",
    "Un lujo en la montaña. El oxígeno suplementario te devuelve fragmentos de humanidad.",
]

# ── Comer ───────────────────────────────────────────────────────
EAT = [
    "Una ración tibia. El cuerpo agradece el gesto.",
    "Comes lo mínimo. La supervivencia no permite excesos.",
    "El alimento sabe a nada, pero tu cuerpo lo absorbe como un milagro.",
    "Masticas despacio. Cada caloría cuenta aquí arriba.",
    "La comida es un ritual. Un momento de normalidad en medio del caos.",
]

# ── Descender ───────────────────────────────────────────────────
DESCEND = [
    "Desciendes. La presión en tu pecho disminuye con cada metro.",
    "Bajas el ritmo. El valle te recibe con algo de calor residual.",
    "Cada paso hacia abajo es una rendición, pero también una salvación.",
    "La montaña te suelta, metro a metro. El aire se vuelve más amable.",
    "Retrocedes. No es derrota, es estrategia. La montaña estará ahí mañana.",
]

# ── Descansar ───────────────────────────────────────────────────
REST = [
    "Te detienes. Solo un momento, pero el cuerpo lo necesitaba.",
    "Esperas. La inmovilidad pesa, pero el descanso es necesario.",
    "Te sientas sobre la mochila. El viento te recuerda que no puedes quedarte aquí mucho tiempo.",
    "Cierras los ojos un instante. El frío te devuelve a la realidad.",
    "Un respiro. La montaña no espera, pero tu cuerpo sí lo necesita.",
]

# ── Willpower bajo ──────────────────────────────────────────────
LOW_WILLPOWER = [
    "La mente vagabundea. El suelo parece más cercano de lo que debería.",
    "La voluntad se erosiona. Cada paso es una duda.",
    "Piensas en rendirte. No es un pensamiento nuevo, pero hoy pesa más.",
    "Las sombras se alargan. No sabes si es el cansancio o algo más.",
    "Tu reflejo en el hielo te devuelve una mirada que no reconoces.",
    "El silencio te habla. Dice cosas que no quieres escuchar.",
]

# ── Zona de la Muerte ───────────────────────────────────────────
DEATH_ZONE = [
    "La zona de la muerte no perdona. El cuerpo consume sus propias reservas.",
    "Pasas los 8000 metros. El oxígeno es un lujo y el tiempo se agota.",
    "Cada célula de tu cuerpo grita que bajes. Pero la cima está tan cerca.",
    "El aire es tan delgado que respirar duele. Sigues adelante.",
    "La montaña te ha absorbido. Ya no eres un escalador, eres parte del hielo.",
    "Los cuerpos de otros escaladores marcan el camino. Ninguno llegó a la cima.",
]

# ── Tormenta ────────────────────────────────────────────────────
STORM = [
    "La tormenta te envuelve. Visibilidad cero.",
    "El viento aúlla. La nieve golpea tu rostro sin piedad.",
    "No ves nada más allá de tu nariz. El mundo se reduce a blanco y dolor.",
    "La tormenta no distingue entre preparados y desprevenidos. Todos sufren igual.",
    "El frío penetra hasta los huesos. La tormenta no tiene piedad.",
]

# ── Suffixes contextuales ───────────────────────────────────────
SUFFIXES = {
    "general": [
        "El K2 no perdona.",
        "La montaña exige.",
        "Cada turno cuenta.",
        "El tiempo corre contra ti.",
        "La cima es una promesa, no una garantía.",
    ],
    "desperation": [
        "¿Cuánto más puedes aguantar?",
        "El cuerpo tiene límites. La mente, también.",
        "Cada paso podría ser el último.",
        "La montaña no te extrañará si te quedas aquí.",
    ],
    "hope": [
        "La cima está más cerca de lo que parece.",
        "Un paso más. Siempre un paso más.",
        "El sol sale para todos, incluso aquí arriba.",
        "La montaña te prueba, pero no te ha vencido.",
    ],
}

# ── Epitafios ───────────────────────────────────────────────────
EPITAPHS = {
    "DEAD_EXHAUSTION": [
        "Tu cuerpo se rindió antes que tu voluntad. La montaña respetó tu esfuerzo.",
        "El agotamiento te alcanzó. No fue falta de coraje, fue falta de aire.",
        "Caminaste hasta que tus piernas dejaron de obedecer. La montaña recuerda tu nombre.",
    ],
    "DEAD_COLD": [
        "El frío te reclamó. Tu cuerpo se convirtió en parte del glaciar.",
        "La hipotermia fue silenciosa. Te dormiste en la nieve y no despertaste.",
        "El hielo te abrazó. Ahora eres parte eterna de la montaña.",
    ],
    "DEAD_FALL": [
        "La gravedad fue más rápida que tu reflejo. El abismo te recibió sin preguntas.",
        "Un paso en falso. Eso fue todo. La montaña no perdona distracciones.",
        "Caíste. El eco de tu grito se perdió en el viento.",
    ],
    "DEAD_STORM": [
        "La tormenta fue más fuerte que tu voluntad. El viento te arrancó de la montaña.",
        "No viste venir la ráfaga. La montaña te devolvió al valle en un instante.",
        "La ventisca te tragó. Ni tus huellas quedaron.",
    ],
    "DEAD_EDEMA": [
        "Tus pulmones se llenaron de líquido. La altitud te traicionó desde dentro.",
        "El edema pulmonar fue implacable. Cada respiración era un suplicio.",
        "Tu cuerpo no pudo con la altura. El aire se volvió tu enemigo.",
    ],
    "default": [
        "La montaña te reclamó. Tu nombre se pierde en el viento.",
        "Non Omnis Moriar — No todo de mí morirá en esta montaña.",
        "El K2 me ha reclamado, pero no me ha vencido.",
    ],
}

LATIN_PHRASES = [
    "Non Omnis Moriar.",
    "Ad astra per aspera.",
    "Memento mori.",
    "Dum spiro, spero.",
    "Per aspera ad astra.",
    "Veni, vidi, vici.",
    "Carpe diem.",
    "Alea iacta est.",
]


def _select_from_list(lst: list[str], seed: int | None = None) -> str:
    """Select a random item from a list, optionally seeded for reproducibility."""
    if seed is not None:
        random.seed(seed)
    return random.choice(lst)


def _get_altitude_tier(altitude: float) -> str:
    """Return altitude tier: low, mid, high, death_zone."""
    if altitude >= 8000:
        return "death_zone"
    elif altitude >= 7000:
        return "high"
    elif altitude >= 6000:
        return "mid"
    return "low"


def _get_weather_category(weather: str) -> str:
    """Return weather category for narrative selection."""
    if weather in ("STORM", "WHITEOUT"):
        return "storm"
    elif weather == "CLEAR":
        return "clear"
    return "default"


def _apply_willpower_voice(text: str, willpower: float) -> str:
    """Degrade narrative prose quality based on willpower level."""
    if willpower >= 30:
        return text  # Normal/high willpower: no degradation
    if willpower < 15:
        # DESPAIR: fragments the sentence, adds ellipsis and repetition
        words = text.split()
        if len(words) > 8:
            truncated = " ".join(words[:6])
            return f"{truncated}... no importa."
        return f"{text}..."
    # DOUBT: shortens and adds uncertainty
    sentences = text.split(". ")
    if len(sentences) > 1:
        return sentences[0] + "."
    return text


def generate_narrative(
    action: str,
    deltas: dict,
    event: dict | None,
    willpower: float,
    altitude: float,
    weather: str,
) -> str:
    """Generate composed contextual narrative for a turn.
    
    Narrative structure:
    [action narrative] + optional [delta context] + optional [event narrative]
    These are separate paragraphs, not a single string.
    """
    altitude_tier = _get_altitude_tier(altitude)
    weather_cat = _get_weather_category(weather)
    parts: list[str] = []

    # --- Action narrative ---
    if willpower < 15:
        # DESPAIR: override with low willpower fragments
        action_text = _select_from_list(LOW_WILLPOWER)
    elif altitude_tier == "death_zone":
        action_text = _select_from_list(DEATH_ZONE)
    elif weather_cat == "storm" and action not in ("CAMP", "EAT", "USE_OXYGEN"):
        action_text = _select_from_list(STORM)
    else:
        action_templates = {
            "ADVANCE_NORMAL": ADVANCE_NORMAL.get(altitude_tier, ADVANCE_NORMAL["low"]),
            "ADVANCE_AGGRESSIVE": ADVANCE_AGGRESSIVE.get(altitude_tier, ADVANCE_AGGRESSIVE["low"]),
            "SECURE_ROUTE": SECURE_ROUTE,
            "CAMP": CAMP.get(weather_cat, CAMP["default"]),
            "USE_OXYGEN": USE_OXYGEN,
            "EAT": EAT,
            "DESCEND": DESCEND,
            "REST": REST,
            "intro": INTRO_TEMPLATES,
        }
        templates = action_templates.get(action, ADVANCE_NORMAL["low"])
        action_text = _select_from_list(templates)

    # Apply willpower voice degradation
    action_text = _apply_willpower_voice(action_text, willpower)
    parts.append(action_text)

    # --- Delta context (only meaningful changes) ---
    delta_parts = []
    if deltas.get("stamina_delta", 0) < -25:
        delta_parts.append("El agotamiento se acumula.")
    if deltas.get("temp_delta", 0) < -2.5:
        delta_parts.append("El frío penetra hasta los huesos.")
    if deltas.get("willpower_delta", 0) < -12:
        delta_parts.append("La mente se nubla.")
    if deltas.get("altitude_delta", 0) > 250:
        delta_parts.append("La cima se siente más cerca.")
    if deltas.get("altitude_delta", 0) < -150:
        delta_parts.append("Bajar duele más que subir.")

    if delta_parts and random.random() < 0.6:
        delta_text = _apply_willpower_voice(" ".join(delta_parts), willpower)
        parts[0] = parts[0] + " " + delta_text

    # --- Contextual suffix ---
    if willpower < 20:
        suffix_pool = SUFFIXES["desperation"]
        suffix_chance = 0.55
    elif willpower > 70:
        suffix_pool = SUFFIXES["hope"]
        suffix_chance = 0.35
    else:
        suffix_pool = SUFFIXES["general"]
        suffix_chance = 0.30

    if random.random() < suffix_chance:
        suffix = _select_from_list(suffix_pool)
        suffix = _apply_willpower_voice(suffix, willpower)
        parts[0] = parts[0] + " " + suffix

    # --- Event narrative (separate paragraph, if any) ---
    if event:
        event_text = event.get("narrative", "")
        if event_text:
            parts.append(event_text)

    return "\n\n".join(parts)


def generate_epitaph(
    death_cause: str,
    max_altitude: float,
    turn: int,
    worst_moment: str = "",
) -> str:
    """Generate a poetic epitaph for the fallen climber."""
    cause_epitaphs = EPITAPHS.get(death_cause, EPITAPHS["default"])
    base = _select_from_list(cause_epitaphs)
    latin = _select_from_list(LATIN_PHRASES)

    # Build contextual epitaph
    parts = [base]

    if max_altitude >= 8000:
        parts.append(f"Llegaste a la zona de la muerte ({max_altitude:.0f}m).")
    elif max_altitude >= 7000:
        parts.append(f"Alcanzaste los {max_altitude:.0f}m antes de caer.")
    else:
        parts.append(f"Tu expedición terminó a los {max_altitude:.0f}m.")

    parts.append(f"Sobreviviste {turn} {'hora' if turn == 1 else 'horas'} en la montaña.")

    if worst_moment:
        parts.append(worst_moment)

    parts.append(latin)

    return " ".join(parts)
