import type { GameState, TurnResult } from './types'

// Empty string = relative URLs. Nginx proxies /game/ → backend:8000
// Override with VITE_API_BASE for dev or split deployments
const API_BASE = import.meta.env.VITE_API_BASE || ''

export class HttpError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'HttpError'
    this.status = status
  }
}

export class SessionExpiredError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'SessionExpiredError'
  }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    if (res.status === 410) {
      throw new SessionExpiredError('Session expired')
    }
    throw new HttpError(
      (body as { detail?: string }).detail || `HTTP ${res.status}`,
      res.status,
    )
  }
  return res.json() as Promise<T>
}

export interface NewGameResponse {
  session_id: string
  state: GameState
  narrative: string
  role_display_name?: string
  role_difficulty?: string
}

export function newGame(role?: string): Promise<NewGameResponse> {
  const body = role ? JSON.stringify({ role }) : undefined
  return request<NewGameResponse>('/game/new', {
    method: 'POST',
    ...(body && { body }),
  })
}

export type TurnResponse =
  | { ok: true; data: TurnResult }
  | { ok: false; error: string }

export interface TurnRequest {
  session_id: string
  action: string
}

export async function postTurn(data: TurnRequest): Promise<TurnResponse> {
  try {
    const result = await request<TurnResult>('/game/turn', {
      method: 'POST',
      body: JSON.stringify(data),
    })
    return { ok: true, data: result }
  } catch (e) {
    if (e instanceof HttpError && e.status === 422) {
      return { ok: false, error: e.message }
    }
    throw e
  }
}

export function getState(sessionId: string): Promise<{ state: GameState }> {
  return request<{ state: GameState }>(`/game/state/${sessionId}`)
}

export function deleteSession(sessionId: string): Promise<void> {
  return request<void>(`/game/session/${sessionId}`, { method: 'DELETE' })
}