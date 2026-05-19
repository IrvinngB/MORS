import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { GameState, TurnDeltas, ActionType } from '@/api/types'
import { newGame, postTurn, getState, deleteSession, SessionExpiredError } from '@/api/game'
import { useUiStore } from '@/stores/uiStore'
import router from '@/router'

export const useGameStore = defineStore('game', () => {
  const state = ref<GameState | null>(null)
  const deltas = ref<TurnDeltas | null>(null)
  const lastNarrative = ref<string>('')
  const epitaph = ref<string | null>(null)
  const lastEvent = ref<{ event_type: string; narrative: string } | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const isTerminal = ref(false)
  const currentRole = ref<string>('')
  const roleDisplayName = ref<string>('')

  const sessionId = computed(() => state.value?.session_id ?? null)
  const status = computed(() => state.value?.status ?? null)
  const turn = computed(() => state.value?.turn ?? 0)
  const altitude = computed(() => state.value?.player?.altitude ?? 5200)
  const maxAltitude = computed(() => state.value?.player?.max_altitude_reached ?? 5200)
  const isNight = computed(() => turn.value % 24 >= 12)
  const inDeathZone = computed(() => altitude.value >= 8000)
  const willpowerState = computed(() => {
    const wp = state.value?.player?.willpower ?? 100
    if (wp < 15) return 'DESPAIR'
    if (wp < 30) return 'DOUBT'
    return 'NORMAL'
  })

  async function startGame(role?: string) {
    isLoading.value = true
    error.value = null
    try {
      const res = await newGame(role)
      state.value = res.state
      lastNarrative.value = res.narrative
      currentRole.value = res.state.role ?? ''
      roleDisplayName.value = res.role_display_name ?? ''
      deltas.value = null
      lastEvent.value = null
      isTerminal.value = false
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Failed to start game'
    } finally {
      isLoading.value = false
    }
  }

  async function resumeGame(id: string) {
    isLoading.value = true
    error.value = null
    try {
      const res = await getState(id)
      state.value = res.state
      const log = res.state.narrative_log
      lastNarrative.value = log[log.length - 1] ?? ''
      deltas.value = null
      lastEvent.value = null
      isTerminal.value = res.state.status !== 'ALIVE'
    } catch (e) {
      if (e instanceof SessionExpiredError) {
        localStorage.removeItem('mors_session_id')
        router.push('/')
        return
      }
      error.value = e instanceof Error ? e.message : 'Failed to resume game'
    } finally {
      isLoading.value = false
    }
  }

  async function takeTurn(action: ActionType) {
    if (!state.value || isLoading.value) return
    isLoading.value = true
    error.value = null
    try {
      const res = await postTurn({ session_id: state.value.session_id, action })
      state.value = res.new_state
      deltas.value = res.deltas
      lastNarrative.value = res.narrative
      lastEvent.value = res.event
      epitaph.value = res.epitaph ?? null
      isTerminal.value = res.is_terminal

      // Show event banner if an event occurred
      if (res.event) {
        const ui = useUiStore()
        ui.triggerEventBanner(res.event.narrative, res.event.event_type)
      }
    } catch (e) {
      if (e instanceof SessionExpiredError) {
        localStorage.removeItem('mors_session_id')
        router.push('/')
        return
      }
      error.value = e instanceof Error ? e.message : 'Turn failed'
    } finally {
      isLoading.value = false
    }
  }

  async function endGame() {
    if (state.value) {
      await deleteSession(state.value.session_id).catch(() => {})
    }
    state.value = null
    deltas.value = null
    lastNarrative.value = ''
    epitaph.value = null
    lastEvent.value = null
    isTerminal.value = false
    error.value = null
  }

  return {
    state,
    deltas,
    lastNarrative,
    epitaph,
    lastEvent,
    isLoading,
    error,
    isTerminal,
    currentRole,
    roleDisplayName,
    sessionId,
    status,
    turn,
    altitude,
    maxAltitude,
    isNight,
    inDeathZone,
    willpowerState,
    startGame,
    resumeGame,
    takeTurn,
    endGame,
  }
})