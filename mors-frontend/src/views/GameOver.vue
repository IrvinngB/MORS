<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useGameStore } from '@/stores/gameStore'
import { useGameLoop } from '@/composables/useGameLoop'

const router = useRouter()
const game = useGameStore()
const { startFresh } = useGameLoop()

const causeLabels: Record<string, string> = {
  DEAD_EXHAUSTION: 'Agotamiento',
  DEAD_COLD: 'Congelamiento',
  DEAD_FALL: 'Caída',
  DEAD_STORM: 'Tormenta',
  DEAD_EDEMA: 'Edema Pulmonar',
}

async function onNewGame() {
  await game.endGame()
  localStorage.removeItem('mors_session_id')
  await startFresh()
  router.push('/game')
}
</script>

<template>
  <div class="min-h-screen bg-mors text-snow flex flex-col items-center justify-center p-8">
    <h1 class="text-6xl font-bold text-danger mb-4">FIN</h1>
    <p class="text-xl text-ice mb-2">{{ causeLabels[game.state?.death_cause ?? ''] || 'Causa desconocida' }}</p>
    <p class="text-ice mb-8">Altitud máxima alcanzada: {{ game.maxAltitude.toFixed(0) }}m</p>

    <div class="bg-peak/50 rounded-lg p-6 mb-8 min-w-96">
      <h2 class="text-lg font-bold text-warning mb-4"> epitafio</h2>
      <p class="text-ice italic text-sm leading-relaxed">
        {{ game.lastNarrative }}
      </p>
    </div>

    <div class="flex gap-4">
      <button
        class="px-6 py-3 bg-danger text-snow font-bold rounded hover:opacity-80 transition"
        @click="onNewGame"
      >
        Intentar de Nuevo
      </button>
      <button
        class="px-6 py-3 border border-snow rounded hover:bg-snow/10 transition"
        @click="router.push('/')"
      >
        Menú Principal
      </button>
    </div>
  </div>
</template>