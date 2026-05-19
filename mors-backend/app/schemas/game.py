from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.game_state import GameState, TurnDeltas, RandomEvent


class NewGameResponse(BaseModel):
    session_id: str
    state: GameState
    narrative: str


class TurnRequest(BaseModel):
    session_id: str
    action: str


class TurnResponse(BaseModel):
    new_state: GameState
    deltas: TurnDeltas
    event: Optional[RandomEvent] = None
    narrative: str
    epitaph: Optional[str] = None
    is_terminal: bool



class StateResponse(BaseModel):
    state: GameState
    turn_count: int
    max_altitude_reached: float
    total_play_time: Optional[str] = None