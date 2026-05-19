import { useGameStore } from '@/stores/gameStore'
import { useUiStore } from '@/stores/uiStore'
import type { ActionType } from '@/api/types'

export function useGameLoop() {
  const game = useGameStore()
  const ui = useUiStore()

  function executeAction(action: ActionType) {
    const COSTLY_ACTIONS: ActionType[] = ['ADVANCE_AGGRESSIVE', 'SECURE_ROUTE', 'CAMP']
    if (COSTLY_ACTIONS.includes(action)) {
      ui.openConfirm(action, `¿Confirmar ${action}?`)
      return
    }
    game.takeTurn(action)
  }

  function confirmAction() {
    const action = ui.confirmAction as ActionType | null
    ui.closeConfirm()
    if (action) game.takeTurn(action)
  }

  async function startOrResume() {
    const stored = localStorage.getItem('mors_session_id')
    if (stored) {
      await game.resumeGame(stored)
    } else {
      await game.startGame()
    }
    if (game.sessionId) {
      localStorage.setItem('mors_session_id', game.sessionId)
    }
  }

  async function startFresh() {
    localStorage.removeItem('mors_session_id')
    await game.startGame()
    if (game.sessionId) {
      localStorage.setItem('mors_session_id', game.sessionId)
    }
  }

  return { executeAction, confirmAction, startOrResume, startFresh }
}