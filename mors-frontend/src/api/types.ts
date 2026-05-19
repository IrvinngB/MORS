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

export interface PlayerStats {
  hp: number
  stamina: number
  body_temp: number
  willpower: number
  altitude: number
  max_altitude_reached: number
  turns_above_8000: number
}

export interface Consumables {
  food_rations: number
  gas_canisters: number
  rope_sections: number
  oxygen_pct: number
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
  is_terminal: boolean
}