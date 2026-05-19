from datetime import datetime, timezone

from app.core import game_engine_process, next_weather, generate_forecast, compute_forecast_reliability
from app.models.enums import ActionType, WeatherState
from app.models.game_state import GameState, TurnDeltas, TurnResult
from app.repositories.memory_repo import MemorySessionRepository
from app.services.event_service import roll_event
from app.services.narrative_service import generate_narrative, generate_epitaph
from app.services.session_service import SessionService


class GameService:
    def __init__(self) -> None:
        self._repo = MemorySessionRepository.get_instance()
        self._session_service = SessionService()

    def new_game(self) -> tuple[GameState, str]:
        state = self._session_service.create_session()

        initial_weather = WeatherState.CLEAR
        forecast = generate_forecast(initial_weather, 1.0)
        state.weather = initial_weather
        state.weather_forecast = forecast
        state.forecast_reliability = 1.0
        self._repo.save(state)

        intro_narrative = generate_narrative(
            action="intro",
            deltas={},
            event=None,
            willpower=state.player.willpower,
            altitude=state.player.altitude,
            weather=state.weather.value if hasattr(state.weather, 'value') else str(state.weather),
        )
        state.narrative_log.append(intro_narrative)
        self._repo.save(state)

        return state, intro_narrative

    def process_turn(self, session_id: str, action_str: str) -> TurnResult:
        state = self._repo.get(session_id)
        if state is None:
            raise ValueError(f"Session {session_id} not found")
        if state.status.value != "ALIVE":
            raise ValueError(f"Session {session_id} is not active")

        try:
            action = ActionType(action_str)
        except ValueError:
            raise ValueError(f"Invalid action: {action_str}")

        new_state, deltas = game_engine_process(state, action)

        if new_state.status.value == "ALIVE":
            next_w = next_weather(WeatherState(new_state.weather))
            reliability = compute_forecast_reliability(
                new_state.player.altitude,
                new_state.turn % 24 >= 12,
                WeatherState(new_state.weather),
            )
            forecast = generate_forecast(next_w, reliability)
            new_state.weather_forecast = forecast
            new_state.forecast_reliability = reliability
            new_state.weather = next_w

        event = roll_event(new_state)
        if event:
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
                new_state.player.hp = max(0.0, min(100.0, new_state.player.hp + event.get("hp_delta", 0)))
            if event.get("stamina_delta"):
                new_state.player.stamina = max(0.0, min(100.0, new_state.player.stamina + event.get("stamina_delta", 0)))
            if event.get("temp_delta"):
                new_state.player.body_temp = max(0.0, min(45.0, new_state.player.body_temp + event.get("temp_delta", 0)))
            if event.get("willpower_delta"):
                new_state.player.willpower = max(0.0, min(100.0, new_state.player.willpower + event.get("willpower_delta", 0)))
            if event.get("oxygen_delta"):
                new_state.consumables.oxygen_pct = max(0.0, min(100.0, new_state.consumables.oxygen_pct + event.get("oxygen_delta", 0)))
            if event.get("rope_delta"):
                new_state.consumables.rope_sections = max(0, new_state.consumables.rope_sections + event.get("rope_delta", 0))

            if new_state.player.hp <= 0 and new_state.death_cause is None:
                new_state.status = new_state.status.DEAD if hasattr(new_state.status, 'DEAD') else "DEAD"
                new_state.death_cause = "DEAD_EXHAUSTION"

        is_terminal = new_state.status.value in ("DEAD", "SUMMIT", "ABANDONED")

        narrative = generate_narrative(
            action=action_str,
            deltas=deltas.model_dump(),
            event=event,
            willpower=new_state.player.willpower,
            altitude=new_state.player.altitude,
            weather=new_state.weather.value if hasattr(new_state.weather, 'value') else str(new_state.weather),
        )

        if is_terminal and new_state.status.value == "DEAD":
            epitaph = generate_epitaph(
                death_cause=new_state.death_cause.value if hasattr(new_state.death_cause, 'value') else str(new_state.death_cause),
                max_altitude=new_state.player.max_altitude_reached,
                turn=new_state.turn,
                worst_moment="La voluntad se rindió.",
            )
            narrative = f"{narrative}\n\n{epitaph}"

        new_state.narrative_log.append(narrative)
        new_state.updated_at = datetime.now(timezone.utc)
        self._repo.save(new_state)

        return TurnResult(
            new_state=new_state,
            deltas=deltas,
            event=event,
            narrative=narrative,
            is_terminal=is_terminal,
        )

    def get_state(self, session_id: str) -> GameState | None:
        return self._repo.get(session_id)