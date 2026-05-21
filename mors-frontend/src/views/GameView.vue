<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useGameStore } from '@/stores/gameStore'
import { useUiStore } from '@/stores/uiStore'
import { useGameLoop } from '@/composables/useGameLoop'
import StatsPanel from '@/components/hud/StatsPanel.vue'
import AltitudeIndicator from '@/components/hud/AltitudeIndicator.vue'
import WeatherWidget from '@/components/hud/WeatherWidget.vue'
import TurnCounter from '@/components/hud/TurnCounter.vue'
import ActionPanel from '@/components/gameplay/ActionPanel.vue'
import ResourceGrid from '@/components/gameplay/ResourceGrid.vue'
import EventBanner from '@/components/gameplay/EventBanner.vue'
import NarrativeLog from '@/components/narrative/NarrativeLog.vue'
import ConfirmModal from '@/components/shared/ConfirmModal.vue'

const router = useRouter()
const game = useGameStore()
const ui = useUiStore()
const { confirmAction, startFresh } = useGameLoop()

const isStormy = computed(() => {
  const w = game.state?.weather
  return w === 'STORM' || w === 'WHITEOUT'
})

async function onNewGame() {
  await game.endGame()
  localStorage.removeItem('mors_session_id')
  await startFresh()
}

function onGoToMenu() {
  game.endGame()
  router.push('/')
}
</script>

<template>
  <div
    class="min-h-screen text-snow flex flex-col relative overflow-hidden"
    :class="[
      game.inDeathZone
        ? 'bg-gradient-to-b from-peak via-mors to-death-zone/20 death-zone-inset'
        : game.isNight
          ? 'bg-gradient-to-b from-abyss via-[#08081a] to-peak/10'
          : 'bg-gradient-to-b from-abyss via-mors to-peak/20',
      game.willpowerState === 'DESPAIR' ? 'despair-overlay' : '',
      isStormy ? 'storm-shake' : '',
    ]"
  >
    <!-- Death zone: thin red border at top -->
    <div
      v-if="game.inDeathZone"
      class="absolute top-0 left-0 right-0 h-px bg-danger/60 animate-pulse z-50"
    />

    <!-- Night overlay: enhanced vignette -->
    <div
      v-if="game.isNight"
      class="absolute inset-0 pointer-events-none night-vignette"
    />

    <!-- Death zone: snow particles -->
    <div v-if="game.inDeathZone" class="absolute inset-0 pointer-events-none overflow-hidden opacity-30">
      <div
        v-for="i in 60"
        :key="i"
        class="snow-particle"
        :style="{
          left: `${Math.random() * 100}%`,
          animationDelay: `${Math.random() * 5}s`,
          animationDuration: `${3 + Math.random() * 5}s`,
          width: `${Math.random() < 0.3 ? 3 : 2}px`,
          height: `${Math.random() < 0.3 ? 3 : 2}px`,
        }"
      />
    </div>

    <!-- Despair: desaturating overlay -->
    <div
      v-if="game.willpowerState === 'DESPAIR'"
      class="absolute inset-0 pointer-events-none bg-danger/5 mix-blend-color-burn"
    />

    <EventBanner />
    <ConfirmModal @confirm="confirmAction" @cancel="ui.closeConfirm" />

    <!-- Header -->
    <header class="relative z-10 flex items-center justify-between px-6 py-3 glass-strong border-b border-white/5">
      <button
        class="text-sm text-ice hover:text-snow transition-colors duration-200 flex items-center gap-2"
        @click="onGoToMenu"
      >
        <span class="text-lg">←</span>
        <span class="hidden sm:inline">Menú</span>
      </button>

      <div class="flex items-center gap-3">
        <span
          v-if="game.currentRole"
          class="text-xs px-2 py-0.5 rounded-full bg-ice/10 text-ice border border-ice/20 font-medium tracking-wide"
        >
          {{ game.roleDisplayName || game.currentRole }}
        </span>
        <TurnCounter />
      </div>

      <button
        v-if="game.isTerminal"
        class="text-sm text-warning hover:text-snow transition-colors duration-200 font-medium"
        @click="onNewGame"
      >
        Nueva Partida
      </button>
    </header>

    <!-- Main content -->
    <main class="relative z-10 flex-1 grid grid-cols-1 lg:grid-cols-[300px_1fr_300px] gap-4 p-4 lg:p-6 max-w-7xl mx-auto w-full">
      <!-- Left sidebar -->
      <aside class="flex flex-col gap-4 order-2 lg:order-1">
        <div class="card" :class="game.inDeathZone ? 'stats-death-zone' : ''">
          <StatsPanel />
        </div>
        <div class="card">
          <AltitudeIndicator />
        </div>
        <div class="card">
          <WeatherWidget />
        </div>
      </aside>

      <!-- Center content -->
      <section class="flex flex-col gap-4 order-1 lg:order-2 min-h-0 max-h-[calc(100vh-5rem)]">
        <!-- Resources pinned at top - always visible -->
        <div class="card shrink-0">
          <ResourceGrid />
        </div>
        <!-- Narrative log fills remaining space, scrolls internally -->
        <div class="card flex-1 min-h-0 overflow-hidden">
          <NarrativeLog />
        </div>
      </section>

      <!-- Right sidebar -->
      <aside class="order-3">
        <div
          class="card"
          :class="game.willpowerState === 'DESPAIR' ? 'despair-panel' : game.willpowerState === 'DOUBT' ? 'doubt-panel' : ''"
        >
          <ActionPanel />
        </div>
      </aside>
    </main>
  </div>
</template>

<style scoped>
/* Despair state: panel with trembling border */
.despair-panel {
  border-color: rgba(231, 76, 60, 0.3) !important;
  animation: despair-shake 8s ease-in-out infinite;
}

@keyframes despair-shake {
  0%, 100% { transform: translateX(0); }
  92%       { transform: translateX(-1px); }
  93%       { transform: translateX(1px); }
  94%       { transform: translateX(-1px); }
  95%       { transform: translateX(0); }
}

/* Doubt state: slightly dimmed panel */
.doubt-panel {
  opacity: 0.92;
  filter: saturate(0.85);
}
</style>
