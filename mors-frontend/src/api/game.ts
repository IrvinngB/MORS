import type { GameState, TurnResult } from './types'

const API_BASE = 'http://localhost:8000'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error((body as { detail?: string }).detail || `HTTP ${res.status}`)
  }
  return res.json() as Promise<T>
}

export interface NewGameResponse {
  session_id: string
  state: GameState
  narrative: string
}

export function newGame(): Promise<NewGameResponse> {
  return request<NewGameResponse>('/game/new', { method: 'POST' })
}

export interface TurnRequest {
  session_id: string
  action: string
}

export function postTurn(data: TurnRequest): Promise<TurnResult> {
  return request<TurnResult>('/game/turn', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function getState(sessionId: string): Promise<{ state: GameState }> {
  return request<{ state: GameState }>(`/game/state/${sessionId}`)
}

export function deleteSession(sessionId: string): Promise<void> {
  return request<void>(`/game/session/${sessionId}`, { method: 'DELETE' })
}