from datetime import datetime, timezone

from app.core import game_engine_process, next_weather, generate_forecast, compute_forecast_reliability
from app.models.enums import ActionType, SessionStatus, WeatherState
from app.models.game_state import GameState, TurnDeltas, TurnResult
from app.models.roles import RoleSpecialAbility
from app.models.roles_registry import ROLES
from app.repositories.memory_repo import MemorySessionRepository
from app.services.event_service import roll_event
from app.services.narrative_service import generate_narrative, generate_epitaph, generate_summit_narrative
from app.services.session_service import SessionService


class SessionExpiredError(Exception):
    """Raised when a session exists but has exceeded its TTL."""
    pass


class GameService:
    def __init__(self) -> None:
        self._repo = MemorySessionRepository.get_instance()
        self._session_service = SessionService()

    def new_game(self, role_id: str = "") -> tuple[GameState, str]:
        state = self._session_service.create_session(role_id=role_id)

        initial_weather = WeatherState.CLEAR
        # Apply forecast reliability bonus for Investigador
        forecast_bonus = 0.0
        if role_id and role_id in ROLES:
            role_def = ROLES[role_id]
            if role_def.special_ability == RoleSpecialAbility.INVESTIGATOR_FORECAST:
                forecast_bonus = role_def.ability_params.get("forecast_reliability_bonus", 0.0)

        base_reliability = 1.0
        forecast_reliability = min(1.0, base_reliability + forecast_bonus)
        forecast = generate_forecast(initial_weather, forecast_reliability)
        state.weather = initial_weather
        state.weather_forecast = forecast
        state.forecast_reliability = forecast_reliability
        self._repo.save(state)

        intro_narrative = generate_narrative(
            action="intro",
            deltas={},
            event=None,
            willpower=state.player.willpower,
            altitude=state.player.altitude,
            weather=state.weather.value if hasattr(state.weather, 'value') else str(state.weather),
            role=role_id,
        )
        state.narrative_log.append(intro_narrative)
        self._repo.save(state)

        return state, intro_narrative

    def _get_hp_mitigation(self, state: GameState) -> float:
        """Get HP event mitigation factor from role. Returns 0.0 (no mitigation) by default."""
        if not state.role or state.role not in ROLES:
            return 0.0
        role_def = ROLES[state.role]
        if role_def.special_ability == RoleSpecialAbility.MEDICO_FREE_HEAL:
            return role_def.ability_params.get("hp_event_mitigation", 0.0)
        return 0.0

    def process_turn(self, session_id: str, action_str: str) -> TurnResult:
        if self._repo.is_expired(session_id):
            raise SessionExpiredError("Session expired")
        state = self._repo.get(session_id)
        if state is None:
            raise ValueError(f"Session {session_id} not found")
        if state.status.value != "ALIVE":
            raise ValueError(f"Session {session_id} is not active")

        try:
            action = ActionType(action_str)
        except ValueError:
            raise ValueError(f"Invalid action: {action_str}")

        prev_event_type = state.last_event_type

        new_state, deltas, warnings = game_engine_process(state, action)

        # Advance weather only if still alive
        if new_state.status.value == "ALIVE":
            next_w = next_weather(WeatherState(new_state.weather))
            reliability = compute_forecast_reliability(
                new_state.player.altitude,
                new_state.turn % 24 >= 12,
                WeatherState(new_state.weather),
            )
            # Apply forecast reliability bonus (Investigador)
            if new_state.role and new_state.role in ROLES:
                role_def = ROLES[new_state.role]
                if role_def.special_ability == RoleSpecialAbility.INVESTIGATOR_FORECAST:
                    bonus = role_def.ability_params.get("forecast_reliability_bonus", 0.0)
                    reliability = min(1.0, reliability + bonus)

            forecast = generate_forecast(next_w, reliability)
            new_state.weather_forecast = forecast
            new_state.forecast_reliability = reliability
            new_state.weather = next_w

        # Roll contextual event — pass last_action for context-aware filtering
        event = roll_event(new_state, last_action=action_str)
        if event:
            # Apply HP event mitigation (Medico)
            hp_mitigation = self._get_hp_mitigation(new_state)
            raw_hp_delta = event.get("hp_delta", 0)
            if raw_hp_delta and hp_mitigation > 0:
                # Reduce damage: damage × (1 - mitigation)
                mitigated_hp = raw_hp_delta * (1 - hp_mitigation)
                event["hp_delta"] = mitigated_hp

            ev_deltas = {
                "hp_delta": event.get("hp_delta", 0),
                "stamina_delta": event.get("stamina_delta", 0),
                "temp_delta": event.get("temp_delta", 0),
                "willpower_delta": event.get("willpower_delta", 0),
                "oxygen_delta": event.get("oxygen_delta", 0),
            }
            for k, v in ev_deltas.items():
                if v:
                    setattr(deltas, k, getattr(deltas, k) + v)

            if event.get("hp_delta"):
                new_state.player.hp = max(0.0, min(100.0, new_state.player.hp + event["hp_delta"]))
            if event.get("stamina_delta"):
                new_state.player.stamina = max(0.0, min(100.0, new_state.player.stamina + event["stamina_delta"]))
            if event.get("temp_delta"):
                new_state.player.body_temp = max(0.0, min(38.0, new_state.player.body_temp + event["temp_delta"]))
            if event.get("willpower_delta"):
                new_state.player.willpower = max(0.0, min(100.0, new_state.player.willpower + event["willpower_delta"]))
            if event.get("oxygen_delta"):
                new_state.consumables.oxygen_pct = max(0.0, min(100.0, new_state.consumables.oxygen_pct + event["oxygen_delta"]))
            if event.get("rope_delta"):
                new_state.consumables.rope_sections = max(0, new_state.consumables.rope_sections + event["rope_delta"])

            if new_state.player.hp <= 0 and new_state.death_cause is None:
                new_state.status = SessionStatus.DEAD if hasattr(new_state.status, 'DEAD') else new_state.status
                event_type = event.get("event_type", "")
                if event_type == "PULMONARY_EDEMA":
                    new_state.death_cause = "DEAD_EDEMA"
                elif event_type in ("TENT_COLLAPSE", "WIND_GUST"):
                    new_state.death_cause = "DEAD_STORM"
                else:
                    new_state.death_cause = "DEAD_EXHAUSTION"

            new_state.last_event_type = event.get("event_type")
        else:
            new_state.last_event_type = None

        # Final death check
        if new_state.player.hp <= 0 and new_state.status.value == "ALIVE":
            new_state.status = new_state.status.__class__("DEAD")

        is_terminal = new_state.status.value in ("DEAD", "SUMMIT", "ABANDONED")

        # Generate turn narrative — pass role for voice modifier
        # Anti-repetition: pass the last narrative so the engine can avoid repeating
        last_narrative = state.narrative_log[-1] if state.narrative_log else None
        narrative = generate_narrative(
            action=action_str,
            deltas=deltas.model_dump(),
            event=event,
            willpower=new_state.player.willpower,
            altitude=new_state.player.altitude,
            weather=new_state.weather.value if hasattr(new_state.weather, 'value') else str(new_state.weather),
            role=new_state.role,
            last_event_type=prev_event_type,
            turn=new_state.turn,
            last_narrative=last_narrative,
        )

        # Generate epitaph or summit narrative separately (not appended to narrative)
        epitaph = None
        if is_terminal and new_state.status.value == "DEAD":
            epitaph = generate_epitaph(
                death_cause=new_state.death_cause.value if hasattr(new_state.death_cause, 'value') else str(new_state.death_cause),
                max_altitude=new_state.player.max_altitude_reached,
                turn=new_state.turn,
                worst_moment="",
                role=new_state.role,
            )
        elif is_terminal and new_state.status.value == "SUMMIT":
            epitaph = generate_summit_narrative(
                role=new_state.role,
                stamina=new_state.player.stamina,
                hp=new_state.player.hp,
            )

        new_state.narrative_log.append(narrative)
        new_state.updated_at = datetime.now(timezone.utc)
        self._repo.save(new_state)

        return TurnResult(
            new_state=new_state,
            deltas=deltas,
            event=event,
            narrative=narrative,
            epitaph=epitaph,
            is_terminal=is_terminal,
            warnings=warnings,
        )

    def get_state(self, session_id: str) -> GameState | None:
        if self._repo.is_expired(session_id):
            raise SessionExpiredError("Session expired")
        return self._repo.get(session_id)
