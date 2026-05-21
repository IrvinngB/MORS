export type WeatherState = 'CLEAR' | 'CLOUDY' | 'WIND' | 'STORM' | 'WHITEOUT'
export type SessionStatus = 'ALIVE' | 'DEAD' | 'SUMMIT' | 'ABANDONED'
export type ActionType =
  | 'ADVANCE_NORMAL'
  | 'ADVANCE_AGGRESSIVE'
  | 'SECURE_ROUTE'
  | 'CAMP'
  | 'USE_OXYGEN'
  | 'EAT'
  | 'DESCEND'
  | 'REST'
  | 'USE_FREE_HEAL'
  | 'TOGGLE_OXYGEN'

export interface RoleDefinition {
  id: string
  display_name: string
  difficulty: 'Easy' | 'Medium' | 'Normal' | 'Hard'
  hp_delta: number
  stamina_delta: number
  willpower_delta: number
  stamina_cost_multiplier: number
  starting_equipment: Record<string, number>
  special_ability: string
  ability_params: Record<string, unknown>
  description: string
}

export interface PlayerStats {
  hp: number
  stamina: number
  body_temp: number
  willpower: number
  altitude: number
  max_altitude_reached: number
  turns_above_8000: number
  entered_death_zone: boolean
  consecutive_aggressive_actions: number
}


export interface Consumables {
  food_rations: number
  gas_canisters: number
  oxygen_tanks: number
  rope_sections: number
  oxygen_pct: number
  oxygen_valve_open: boolean
}

export interface GameState {
  session_id: string
  status: SessionStatus
  turn: number
  player: PlayerStats
  consumables: Consumables
  weather: WeatherState
  weather_forecast: WeatherState
  forecast_reliability: number
  route_secured: number
  death_cause: string | null
  narrative_log: string[]
  created_at: string
  updated_at: string
  role: string
  free_heal_used: boolean
}

export interface TurnDeltas {
  hp_delta: number
  stamina_delta: number
  temp_delta: number
  willpower_delta: number
  altitude_delta: number
  oxygen_delta: number
  route_secured_delta: number
}

export interface TurnResult {
  new_state: GameState
  deltas: TurnDeltas
  event: { event_type: string; narrative: string } | null
  narrative: string
  epitaph: string | null
  warnings: string[]
  is_terminal: boolean
}