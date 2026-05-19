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
  <div class="min-h-screen bg-peak text-snow flex flex-col items-center justify-center p-8">
    <h1 class="text-6xl font-bold text-success mb-4">CIMA</h1>
    <p class="text-xl text-ice mb-8">Has alcanzado los 8.611m del K2</p>

    <div class="bg-mors rounded-lg p-6 mb-8 min-w-96">
      <h2 class="text-lg font-bold text-glacier mb-4">Resumen de Expedición</h2>
      <dl class="grid grid-cols-2 gap-4 text-sm">
        <dt class="text-ice">Turnos</dt>
        <dd>{{ game.turn }}</dd>
        <dt class="text-ice">Altitud Máxima</dt>
        <dd>{{ game.maxAltitude.toFixed(0) }}m</dd>
        <dt class="text-ice">Estado Final</dt>
        <dd>{{ game.status }}</dd>
      </dl>
    </div>

    <div class="flex gap-4">
      <button
        class="px-6 py-3 bg-glacier text-mors font-bold rounded hover:bg-ice transition"
        @click="onNewGame"
      >
        Nueva Expedición
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