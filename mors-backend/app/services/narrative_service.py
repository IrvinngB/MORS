import random
from app.services.narrative import general
from app.services.narrative import role_sherpa
from app.services.narrative import role_clasico
from app.services.narrative import role_investigador
from app.services.narrative import role_tecnico
from app.services.narrative import role_medico

# ═══════════════════════════════════════════════════════════════
# DYNAMICALLY ASSEMBLED DICTIONARIES (For backward & code compatibility)
# ═══════════════════════════════════════════════════════════════

ROLE_VOICE: dict[str, dict] = {
    "sherpa": {
        "prefixes": role_sherpa.PREFIXES,
        "suffixes": role_sherpa.SUFFIXES,
    },
    "clasico": {
        "prefixes": role_clasico.PREFIXES,
        "suffixes": role_clasico.SUFFIXES,
    },
    "investigador": {
        "prefixes": role_investigador.PREFIXES,
        "suffixes": role_investigador.SUFFIXES,
    },
    "tecnico": {
        "prefixes": role_tecnico.PREFIXES,
        "suffixes": role_tecnico.SUFFIXES,
    },
    "medico": {
        "prefixes": role_medico.PREFIXES,
        "suffixes": role_medico.SUFFIXES,
    },
}

# General templates (imported directly from general submodule)
INTRO_TEMPLATES = general.INTRO_TEMPLATES
ADVANCE_NORMAL = general.ADVANCE_NORMAL
ADVANCE_AGGRESSIVE = general.ADVANCE_AGGRESSIVE
SECURE_ROUTE = general.SECURE_ROUTE
CAMP = general.CAMP
USE_OXYGEN = general.USE_OXYGEN
EAT = general.EAT
DESCEND = general.DESCEND
REST = general.REST
FREE_HEAL = general.FREE_HEAL
TOGGLE_OXYGEN = general.TOGGLE_OXYGEN

LOW_WILLPOWER_DESPAIR = general.LOW_WILLPOWER_DESPAIR
LOW_WILLPOWER_DOUBT = general.LOW_WILLPOWER_DOUBT
DEATH_ZONE = general.DEATH_ZONE
STORM = general.STORM
SUFFIXES = general.SUFFIXES
EPITAPHS = general.EPITAPHS
MOUNTAINEERING_QUOTES = general.MOUNTAINEERING_QUOTES
NEPALI_PHRASES = general.NEPALI_PHRASES
POST_EVENT_OVERRIDES = general.POST_EVENT_OVERRIDES
NIGHT_FLAVOR = general.NIGHT_FLAVOR
SUMMIT_CONDITIONS = general.SUMMIT_CONDITIONS

# Role-specific epitaph suffixes mapping
ROLE_EPITAPH_SUFFIX: dict[str, list[str]] = {
    "sherpa": role_sherpa.EPITAPH_SUFFIXES,
    "clasico": role_clasico.EPITAPH_SUFFIXES,
    "investigador": role_investigador.EPITAPH_SUFFIXES,
    "tecnico": role_tecnico.EPITAPH_SUFFIXES,
    "medico": role_medico.EPITAPH_SUFFIXES,
}

# Role-specific summit narratives mapping
SUMMIT_NARRATIVE: dict[str, list[str]] = {
    "default": [
        "La cima. 8611 metros. El mundo entero bajo tus pies.",
        "Llegaste. El K2, el asesino, el salvaje — rendido ante tu voluntad.",
        "8611 metros. Cada paso del camino te trajo aquí. Ahora el cielo es tu techo.",
        "La cima del K2. Donde otros murieron, tú llegaste.",
    ],
    "sherpa": role_sherpa.SUMMIT_NARRATIVES,
    "clasico": role_clasico.SUMMIT_NARRATIVES,
    "investigador": role_investigador.SUMMIT_NARRATIVES,
    "tecnico": role_tecnico.SUMMIT_NARRATIVES,
    "medico": role_medico.SUMMIT_NARRATIVES,
}

# SUMMIT_CONDITIONS now imported from general submodule


# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def _select_from_list(lst: list[str], seed: int | None = None, exclude: list[str] | None = None) -> str:
    """Select a random item from a list, optionally seeded for reproducibility.
    
    Args:
        lst: Pool of strings to choose from.
        seed: Optional random seed for reproducibility.
        exclude: List of strings to exclude from selection (anti-repetition).
                 If exclusion leaves no candidates, falls back to the full pool.
    """
    if seed is not None:
        random.seed(seed)
    candidates = lst
    if exclude:
        candidates = [item for item in lst if item not in exclude]
        if not candidates:
            candidates = lst  # fallback if all excluded
    return random.choice(candidates)


def _get_altitude_tier(altitude: float) -> str:
    """Return altitude tier: low, mid, high, death_zone."""
    if altitude >= 8000:
        return "death_zone"
    elif altitude >= 7000:
        return "high"
    elif altitude >= 6000:
        return "mid"
    return "low"


def _get_willpower_tier(altitude: float) -> str:
    """Return willpower altitude tier: low, mid, high.

    Willpower dicts use 3 tiers (low < 6000m, mid 6000-7999m, high >= 8000m)
    which differ from the standard 4-tier altitude system.
    """
    if altitude >= 8000:
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
    if willpower >= 50:
        return text  # Normal: no degradation
    if willpower >= 30:
        # PURPOSE DOUBT: adds a questioning undertone
        if random.random() < 0.3:
            return text + " ¿Para qué?"
        return text
    if willpower >= 15:
        # DOUBT: shortens and adds uncertainty
        sentences = text.split(". ")
        if len(sentences) > 1:
            return sentences[0] + "."
        return text + " Tal vez."
    # DESPAIR: fragments the sentence, adds ellipsis and repetition
    words = text.split()
    if len(words) > 8:
        truncated = " ".join(words[:6])
        return f"{truncated}... no importa."
    return f"{text}..."


def _apply_role_voice(
    text: str,
    role: str,
    willpower: float,
    altitude: float,
    exclude_prefix: list[str] | None = None,
    exclude_suffix: list[str] | None = None,
) -> str:
    """Apply role-specific voice modifier (prefix/suffix) to narrative text.
    
    This is NOT a rewrite — it's a tone overlay. The same action feels different
    depending on who's experiencing it.
    
    Args:
        exclude_prefix: Prefix strings to skip (anti-repetition).
        exclude_suffix: Suffix strings to skip (anti-repetition).
    """
    if not role or role not in ROLE_VOICE:
        return text

    voice = ROLE_VOICE[role]

    # Low willpower reduces the chance of voice modifiers (mind is too broken for persona)
    if willpower < 15:
        if random.random() < 0.7:  # 70% chance to skip voice at despair
            return text

    # Map altitude to granular tier
    if altitude >= 8000:
        tier = "death_zone"
    elif altitude >= 7000:
        tier = "high"
    elif altitude >= 6000:
        tier = "mid"
    else:
        tier = "low"

    prefixes = voice["prefixes"].get(tier, voice["prefixes"]["low"])
    suffixes = voice["suffixes"].get(tier, voice["suffixes"]["low"])

    prefix = _select_from_list(prefixes, exclude=exclude_prefix)
    suffix = _select_from_list(suffixes, exclude=exclude_suffix)

    return f"{prefix}{text}{suffix}"


# ═══════════════════════════════════════════════════════════════
# EXPOSED ENGINE INTERFACE
# ═══════════════════════════════════════════════════════════════

def generate_narrative(
    action: str,
    deltas: dict,
    event: dict | None,
    willpower: float,
    altitude: float,
    weather: str,
    role: str = "",
    last_event_type: str | None = None,
    turn: int = 0,
    last_narrative: str | None = None,
) -> str:
    """Generate composed contextual narrative for a turn.
    
    Narrative structure:
    [role voice prefix] + [action narrative] + optional [delta context] + optional [suffix]
    These are composed into a single paragraph. Event narrative is a separate paragraph.
    
    Args:
        last_narrative: The narrative string from the previous turn. Used to avoid
            repeating the same action text, prefix, or suffix back-to-back.
    """
    altitude_tier = _get_altitude_tier(altitude)
    weather_cat = _get_weather_category(weather)

    # --- Anti-repetition: extract components from last narrative for exclusion ---
    _exclude_action: list[str] = []
    _exclude_prefix: list[str] = []
    _exclude_suffix: list[str] = []
    if last_narrative:
        # Strip to first paragraph (before event) and remove willpower degradation artifacts
        first_para = last_narrative.split("\n\n")[0]
        # Collect non-empty role prefixes/suffixes that might appear in last narrative
        if role and role in ROLE_VOICE:
            voice = ROLE_VOICE[role]
            tier_key = (
                "death_zone" if altitude >= 8000 else
                "high" if altitude >= 7000 else
                "mid" if altitude >= 6000 else
                "low"
            )
            all_prefixes = voice["prefixes"].get(tier_key, voice["prefixes"]["low"])
            all_suffixes = voice["suffixes"].get(tier_key, voice["suffixes"]["low"])
            for p in all_prefixes:
                if p and p in first_para:
                    _exclude_prefix.append(p)
            for s in all_suffixes:
                if s and s in first_para:
                    _exclude_suffix.append(s)

    # --- Action narrative ---
    willpower_tier = _get_willpower_tier(altitude)
    if willpower < 15:
        # DESPAIR: override with low willpower fragments (altitude-tiered)
        despair_pool = LOW_WILLPOWER_DESPAIR.get(willpower_tier, LOW_WILLPOWER_DESPAIR["low"]) if isinstance(LOW_WILLPOWER_DESPAIR, dict) else LOW_WILLPOWER_DESPAIR
        action_text = _select_from_list(despair_pool, exclude=_exclude_action)
    elif willpower < 50:
        # PURPOSE DOUBT: questioning tone (altitude-tiered)
        doubt_pool = LOW_WILLPOWER_DOUBT.get(willpower_tier, LOW_WILLPOWER_DOUBT["low"]) if isinstance(LOW_WILLPOWER_DOUBT, dict) else LOW_WILLPOWER_DOUBT
        action_text = _select_from_list(doubt_pool, exclude=_exclude_action)
    elif altitude_tier == "death_zone":
        action_text = _select_from_list(DEATH_ZONE, exclude=_exclude_action)
    elif weather_cat == "storm" and action not in ("CAMP", "EAT", "USE_OXYGEN", "USE_FREE_HEAL"):
        action_text = _select_from_list(STORM, exclude=_exclude_action)
    else:
        action_templates = {
            "ADVANCE_NORMAL": ADVANCE_NORMAL.get(altitude_tier, ADVANCE_NORMAL["low"]),
            "ADVANCE_AGGRESSIVE": ADVANCE_AGGRESSIVE.get(altitude_tier, ADVANCE_AGGRESSIVE["low"]),
            "SECURE_ROUTE": SECURE_ROUTE.get(altitude_tier, SECURE_ROUTE["low"]) if isinstance(SECURE_ROUTE, dict) else SECURE_ROUTE,
            "CAMP": CAMP.get(weather_cat, CAMP["default"]),
            "USE_OXYGEN": USE_OXYGEN.get(altitude_tier, USE_OXYGEN["low"]) if isinstance(USE_OXYGEN, dict) else USE_OXYGEN,
            "EAT": EAT.get(altitude_tier, EAT["low"]) if isinstance(EAT, dict) else EAT,
            "DESCEND": DESCEND.get(altitude_tier, DESCEND["low"]) if isinstance(DESCEND, dict) else DESCEND,
            "REST": REST.get(altitude_tier, REST["low"]) if isinstance(REST, dict) else REST,
            "USE_FREE_HEAL": FREE_HEAL.get(altitude_tier, FREE_HEAL["low"]) if isinstance(FREE_HEAL, dict) else FREE_HEAL,
            "TOGGLE_OXYGEN": TOGGLE_OXYGEN.get(altitude_tier, TOGGLE_OXYGEN["low"]) if isinstance(TOGGLE_OXYGEN, dict) else TOGGLE_OXYGEN,
            "intro": INTRO_TEMPLATES,
        }
        templates = action_templates.get(action, ADVANCE_NORMAL.get(altitude_tier, ADVANCE_NORMAL["low"]))
        action_text = _select_from_list(templates, exclude=_exclude_action)

    # --- Night flavor injection ---
    # turn % 24 >= 12 means night. Injected with 35% chance to build night atmosphere.
    if turn % 24 >= 12 and random.random() < 0.35:
        night_text = _select_from_list(NIGHT_FLAVOR)
        action_text = f"{action_text} {night_text}"

    # --- Narrative Memory: continuity from previous turn's event ---
    if last_event_type and last_event_type in POST_EVENT_OVERRIDES:
        if random.random() < 0.65:
            post_event_text = _select_from_list(POST_EVENT_OVERRIDES[last_event_type])
            # Prepend continuity text to action text
            action_text = f"{post_event_text} {action_text}"

    # Apply willpower voice degradation
    action_text = _apply_willpower_voice(action_text, willpower)

    # Apply role voice modifier
    action_text = _apply_role_voice(action_text, role, willpower, altitude, exclude_prefix=_exclude_prefix, exclude_suffix=_exclude_suffix)

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
        action_text = action_text + " " + delta_text

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
        action_text = action_text + " " + suffix

    parts = [action_text]

    # --- Event narrative (separate paragraph, if any) ---
    if event:
        event_text = event.get("narrative", "")
        if event_text:
            parts.append(event_text)

    return "\n\n".join(parts)


def generate_summit_narrative(role: str = "", stamina: float = 100.0, hp: float = 100.0) -> str:
    """Generate narrative for reaching the summit. Varies by role and condition."""
    role_texts = SUMMIT_NARRATIVE.get(role, SUMMIT_NARRATIVE["default"])
    base = _select_from_list(role_texts)

    # Condition suffix
    condition_score = (stamina + hp) / 2
    if condition_score > 85:
        condition = SUMMIT_CONDITIONS["legendary"]
    elif condition_score > 60:
        condition = SUMMIT_CONDITIONS["strong"]
    elif condition_score > 40:
        condition = SUMMIT_CONDITIONS["barely"]
    elif condition_score > 25:
        condition = SUMMIT_CONDITIONS["exhausted"]
    else:
        condition = SUMMIT_CONDITIONS["miracle"]

    # Pick from both mountaineering quotes and Nepali phrases
    all_quotes = MOUNTAINEERING_QUOTES + NEPALI_PHRASES
    quote = _select_from_list(all_quotes)

    return f"{base} {condition}\n\n{quote}"


def generate_epitaph(
    death_cause: str,
    max_altitude: float,
    turn: int,
    worst_moment: str = "",
    role: str = "",
) -> str:
    """Generate a poetic epitaph for the fallen climber. Varies by role."""
    cause_epitaphs = EPITAPHS.get(death_cause, EPITAPHS["default"])
    base = _select_from_list(cause_epitaphs)

    parts = [base]

    # Role-specific epitaph addition
    if role and role in ROLE_EPITAPH_SUFFIX:
        role_suffix = _select_from_list(ROLE_EPITAPH_SUFFIX[role])
        parts.append(role_suffix)

    if max_altitude >= 8000:
        parts.append(f"Llegaste a la zona de la muerte ({max_altitude:.0f}m).")
    elif max_altitude >= 7000:
        parts.append(f"Alcanzaste los {max_altitude:.0f}m antes de caer.")
    else:
        parts.append(f"Tu expedición terminó a los {max_altitude:.0f}m.")

    parts.append(f"Sobreviviste {turn} {'hora' if turn == 1 else 'horas'} en la montaña.")

    if worst_moment:
        parts.append(worst_moment)

    # Pick from both mountaineering quotes and Nepali phrases
    all_quotes = MOUNTAINEERING_QUOTES + NEPALI_PHRASES
    quote = _select_from_list(all_quotes)
    parts.append(quote)

    return " ".join(parts)
