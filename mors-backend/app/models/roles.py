from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class RoleSpecialAbility(str, Enum):
    SHERPA_FALL_RESISTANCE = "sherpa_fall_resistance"
    INVESTIGATOR_FORECAST = "investigator_forecast"
    TECNICO_ALTITUDE_DISCOUNT = "tecnico_altitude_discount"
    MEDICO_FREE_HEAL = "medico_free_heal"
    NONE = "none"


class RoleDefinition(BaseModel):
    id: str
    display_name: str
    difficulty: str  # "Easy" | "Medium" | "Normal" | "Hard"
    hp_delta: int = 0
    stamina_delta: int = 0
    willpower_delta: int = 0
    stamina_cost_multiplier: float = 1.0
    starting_equipment: dict[str, int] = Field(default_factory=dict)
    special_ability: RoleSpecialAbility = RoleSpecialAbility.NONE
    ability_params: dict[str, Any] = Field(default_factory=dict)
    description: str
