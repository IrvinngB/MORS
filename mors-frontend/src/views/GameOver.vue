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

async function onRetry() {
  await game.endGame()
  localStorage.removeItem('mors_session_id')
  await startFresh()
  router.push('/game')
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-abyss via-mors to-danger/10 text-snow flex flex-col items-center justify-center p-8 relative overflow-hidden">
    <!-- Decorative elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/3 left-1/3 w-64 h-64 bg-danger/5 rounded-full blur-3xl" />
      <div class="absolute bottom-1/3 right-1/3 w-96 h-96 bg-peak/20 rounded-full blur-3xl" />
    </div>

    <div class="relative z-10 text-center animate-fade-in max-w-lg w-full">
      <!-- Death icon -->
      <div class="mb-8">
        <svg class="w-20 h-20 mx-auto text-danger/60" viewBox="0 0 100 100" fill="currentColor">
          <circle cx="50" cy="50" r="40" stroke="currentColor" stroke-width="4" fill="none" />
          <path d="M35 35 L65 65 M65 35 L35 65" stroke="currentColor" stroke-width="4" stroke-linecap="round" />
        </svg>
      </div>

      <h1 class="text-6xl md:text-7xl font-black tracking-wider text-danger mb-4">FIN</h1>

      <p class="text-xl text-ice/70 mb-1 font-medium">
        {{ causeLabels[game.state?.death_cause ?? ''] || 'Causa desconocida' }}
      </p>
      <p class="text-sm text-ice/40 mb-10">Altitud máxima: {{ game.maxAltitude.toFixed(0) }}m</p>

      <!-- Last narrative (turn narrative) -->
      <div
        v-if="game.lastNarrative && !game.epitaph"
        class="glass-strong rounded-xl p-6 mb-6 border border-white/10 text-left"
      >
        <h2 class="text-xs font-semibold text-ice/40 uppercase tracking-wider mb-3">Último turno</h2>
        <p class="text-ice/60 text-sm leading-relaxed">{{ game.lastNarrative }}</p>
      </div>

      <!-- Epitaph card (shown when available) -->
      <div
        v-if="game.epitaph"
        class="glass-strong rounded-xl p-6 mb-10 border border-danger/25 text-left"
      >
        <h2 class="text-xs font-semibold text-danger/50 uppercase tracking-wider mb-4">Epitafio</h2>
        <p class="text-ice/70 italic text-sm leading-relaxed font-light">
          {{ game.epitaph }}
        </p>
      </div>

      <!-- Actions -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <button
          id="btn-retry"
          class="btn-danger text-lg tracking-wide"
          @click="onRetry"
        >
          Intentar de Nuevo
        </button>
        <button
          id="btn-menu"
          class="btn-secondary text-lg tracking-wide"
          @click="router.push('/')"
        >
          Menú Principal
        </button>
      </div>
    </div>
  </div>
</template>
