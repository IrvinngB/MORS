<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useGameStore } from '@/stores/gameStore'
import { useGameLoop } from '@/composables/useGameLoop'
import { computed } from 'vue'

const router = useRouter()
const game = useGameStore()
const { startFresh } = useGameLoop()

// The epitaph field contains the summit narrative when status is SUMMIT
const summitNarrative = computed(() => game.epitaph || '')

// Parse the narrative into lines for display (separated by \n\n)
const narrativeLines = computed(() => {
  if (!summitNarrative.value) return []
  return summitNarrative.value.split('\n\n').filter(Boolean)
})

function conditionLabel() {
  const hp = game.state?.player.hp ?? 100
  const stamina = game.state?.player.stamina ?? 100
  const score = (hp + stamina) / 2
  if (score > 60) return 'Expedición dominante'
  if (score > 25) return 'Victoria sufrida'
  return 'Milagro en la montaña'
}

async function onNewGame() {
  await game.endGame()
  localStorage.removeItem('mors_session_id')
  await startFresh()
  router.push('/game')
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-abyss via-[#08081a] to-success/10 text-snow flex flex-col items-center justify-center p-8 relative overflow-hidden">
    <!-- Decorative elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-64 h-64 bg-success/5 rounded-full blur-3xl" />
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-glacier/5 rounded-full blur-3xl" />
    </div>

    <div class="relative z-10 text-center animate-fade-in max-w-2xl">
      <!-- Summit icon -->
      <div class="mb-6">
        <svg class="w-20 h-20 mx-auto text-success/80" viewBox="0 0 100 100" fill="currentColor">
          <path d="M50 10 L70 40 L90 35 L60 60 L80 90 L50 70 L20 90 L40 60 L10 35 L30 40 Z" />
        </svg>
      </div>

      <h1 class="text-5xl md:text-6xl font-black tracking-wider text-success mb-2">CIMA</h1>
      <p class="text-lg text-ice/60 mb-1">8.611m — K2</p>
      <p class="text-sm text-ice/40 italic mb-8">Tunduki pugyo (टुप्पोमा पुग्यो) — Se alcanzó la cumbre</p>

      <!-- Summit narrative from backend -->
      <div
        v-if="narrativeLines.length > 0"
        class="glass-strong rounded-xl p-6 mb-8 border border-success/20 text-left"
      >
        <div
          v-for="(line, i) in narrativeLines"
          :key="i"
          class="text-sm leading-relaxed text-ice/80"
          :class="{ 'text-snow font-medium': i === 0 }"
        >
          {{ line }}
          <br v-if="i < narrativeLines.length - 1" class="mb-3">
        </div>
      </div>

      <!-- Stats card -->
      <div class="glass-strong rounded-xl p-6 mb-10 border border-white/10">
        <div class="flex items-center justify-center gap-2 mb-4">
          <span class="text-xs font-semibold text-success uppercase tracking-wider">{{ conditionLabel() }}</span>
        </div>
        <dl class="grid grid-cols-2 sm:grid-cols-4 gap-6 text-sm">
          <div>
            <dt class="text-ice/50 mb-1 text-xs">Turnos</dt>
            <dd class="text-xl font-mono font-bold text-snow">{{ game.turn }}</dd>
          </div>
          <div>
            <dt class="text-ice/50 mb-1 text-xs">Altitud</dt>
            <dd class="text-xl font-mono font-bold text-snow">{{ game.maxAltitude.toFixed(0) }}m</dd>
          </div>
          <div>
            <dt class="text-ice/50 mb-1 text-xs">HP</dt>
            <dd class="text-xl font-mono font-bold text-snow">{{ game.state?.player.hp.toFixed(0) }}</dd>
          </div>
          <div>
            <dt class="text-ice/50 mb-1 text-xs">Stamina</dt>
            <dd class="text-xl font-mono font-bold text-snow">{{ game.state?.player.stamina.toFixed(0) }}</dd>
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
