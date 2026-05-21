import { useGameStore } from '@/stores/gameStore'
import { useUiStore } from '@/stores/uiStore'
import type { ActionType } from '@/api/types'
import { SessionExpiredError } from '@/api/game'
import router from '@/router'

export function useGameLoop() {
  const game = useGameStore()
  const ui = useUiStore()

  function executeAction(action: ActionType) {
    if (action === 'CAMP' && game.isCampLethal) {
      ui.openConfirm(action, '⚠️ Acampar sin gas en tormenta puede ser LETAL. ¿Confirmar de todos modos?', true)
      return
    }

    const COSTLY_ACTIONS: ActionType[] = ['ADVANCE_AGGRESSIVE', 'SECURE_ROUTE']
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
      try {
        await game.resumeGame(stored)
      } catch (e) {
        if (e instanceof SessionExpiredError) {
          localStorage.removeItem('mors_session_id')
          router.push('/')
          return
        }
        throw e
      }
    } else {
      await game.startGame()
    }
    if (game.sessionId) {
      localStorage.setItem('mors_session_id', game.sessionId)
    }
  }

  async function startFresh(role?: string) {
    localStorage.removeItem('mors_session_id')
    await game.startGame(role)
    if (game.sessionId) {
      localStorage.setItem('mors_session_id', game.sessionId)
    }
  }

  return { executeAction, confirmAction, startOrResume, startFresh }
}
