<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useGameStore } from '@/stores/gameStore'
import { useGameLoop } from '@/composables/useGameLoop'

const router = useRouter()
const game = useGameStore()
const { startFresh } = useGameLoop()

async function onNewGame() {
  await game.endGame()
  localStorage.removeItem('mors_session_id')
  await startFresh()
  router.push('/game')
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-abyss via-mors to-success/10 text-snow flex flex-col items-center justify-center p-8 relative overflow-hidden">
    <!-- Decorative elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-64 h-64 bg-success/5 rounded-full blur-3xl" />
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-glacier/5 rounded-full blur-3xl" />
    </div>

    <div class="relative z-10 text-center animate-fade-in">
      <!-- Summit icon -->
      <div class="mb-8">
        <svg class="w-24 h-24 mx-auto text-success/80" viewBox="0 0 100 100" fill="currentColor">
          <path d="M50 10 L70 40 L90 35 L60 60 L80 90 L50 70 L20 90 L40 60 L10 35 L30 40 Z" />
        </svg>
      </div>

      <h1 class="text-6xl md:text-7xl font-black tracking-wider text-success mb-4">CIMA</h1>
      <p class="text-xl text-ice/70 mb-2">Has alcanzado los 8.611m del K2</p>
      <p class="text-sm text-ice/40 italic mb-12">Non Omnis Moriar</p>

      <!-- Stats card -->
      <div class="glass-strong rounded-xl p-6 mb-10 max-w-md mx-auto border border-success/20">
        <h2 class="text-sm font-semibold text-success/80 uppercase tracking-wider mb-6">Resumen de Expedición</h2>
        <dl class="grid grid-cols-2 gap-6 text-sm">
          <div>
            <dt class="text-ice/50 mb-1">Turnos</dt>
            <dd class="text-2xl font-mono font-bold text-snow">{{ game.turn }}</dd>
          </div>
          <div>
            <dt class="text-ice/50 mb-1">Altitud Máx.</dt>
            <dd class="text-2xl font-mono font-bold text-snow">{{ game.maxAltitude.toFixed(0) }}m</dd>
          </div>
          <div>
            <dt class="text-ice/50 mb-1">HP Final</dt>
            <dd class="text-2xl font-mono font-bold text-snow">{{ game.state?.player.hp.toFixed(0) }}</dd>
          </div>
          <div>
            <dt class="text-ice/50 mb-1">Stamina</dt>
            <dd class="text-2xl font-mono font-bold text-snow">{{ game.state?.player.stamina.toFixed(0) }}</dd>
          </div>
        </dl>
      </div>

      <!-- Actions -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <button
          class="btn-primary text-lg tracking-wide"
          @click="onNewGame"
        >
          Nueva Expedición
        </button>
        <button
          class="btn-secondary text-lg tracking-wide"
          @click="router.push('/')"
        >
          Menú Principal
        </button>
      </div>
    </div>
  </div>
</template>
