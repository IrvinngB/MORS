from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field

from .enums import ActionType, DeathCause, EventType, SessionStatus, WeatherState


class PlayerStats(BaseModel):
    hp: float = Field(default=100.0, ge=0.0, le=100.0)
    stamina: float = Field(default=100.0, ge=0.0, le=100.0)
    body_temp: float = Field(default=37.0, ge=0.0)
    willpower: float = Field(default=100.0, ge=0.0, le=100.0)
    altitude: float = Field(default=5200.0, ge=0.0)
    max_altitude_reached: float = Field(default=5200.0, ge=0.0)
    turns_above_8000: int = Field(default=0, ge=0)


class Consumables(BaseModel):
    food_rations: int = Field(default=10, ge=0)
    gas_canisters: int = Field(default=5, ge=0)
    rope_sections: int = Field(default=3, ge=0)
    oxygen_pct: float = Field(default=100.0, ge=0.0, le=100.0)


class RandomEvent(BaseModel):
    event_type: EventType
    narrative: str


class GameState(BaseModel):
    session_id: str
    status: SessionStatus = SessionStatus.ALIVE
    turn: int = 0
    player: PlayerStats = Field(default_factory=PlayerStats)
    consumables: Consumables = Field(default_factory=Consumables)
    weather: WeatherState = WeatherState.CLEAR
    weather_forecast: WeatherState = WeatherState.CLEAR
    forecast_reliability: float = Field(default=1.0, ge=0.0, le=1.0)
    route_secured: int = 0
    death_cause: Optional[DeathCause] = None
    narrative_log: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    turns_without_stamina_recovery: int = 0

    model_config = {"use_enum_values": True}


class TurnDeltas(BaseModel):
    hp_delta: float = 0.0
    stamina_delta: float = 0.0
    temp_delta: float = 0.0
    willpower_delta: float = 0.0
    altitude_delta: float = 0.0
    oxygen_delta: float = 0.0
    route_secured_delta: int = 0


class TurnResult(BaseModel):
    new_state: GameState
    deltas: TurnDeltas
    event: Optional[RandomEvent] = None
    narrative: str = ""
    is_terminal: bool = False