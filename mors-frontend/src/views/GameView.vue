<script setup lang="ts">
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
    :class="game.inDeathZone ? 'bg-gradient-to-b from-peak via-mors to-death-zone/20' : 'bg-gradient-to-b from-abyss via-mors to-peak/20'"
  >
    <!-- Snow overlay for death zone -->
    <div v-if="game.inDeathZone" class="absolute inset-0 pointer-events-none overflow-hidden opacity-30">
      <div v-for="i in 50" :key="i" 
           class="snow-particle"
           :style="{
             left: `${Math.random() * 100}%`,
             animationDelay: `${Math.random() * 5}s`,
             animationDuration: `${4 + Math.random() * 6}s`,
           }"
      />
    </div>

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
      
      <TurnCounter />
      
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
        <div class="card">
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
      <section class="flex flex-col gap-4 order-1 lg:order-2 min-h-0">
        <div class="card flex-1 min-h-[200px] lg:min-h-0">
          <NarrativeLog />
        </div>
        <div class="card">
          <ResourceGrid />
        </div>
      </section>

      <!-- Right sidebar -->
      <aside class="order-3">
        <div class="card">
          <ActionPanel />
        </div>
      </aside>
    </main>
  </div>
</template>
