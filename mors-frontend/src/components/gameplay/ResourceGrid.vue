<script setup lang="ts">
import { computed } from 'vue'
import { useGameStore } from '@/stores/gameStore'

const game = useGameStore()

const c = computed(() => game.state?.consumables)

const resources = computed(() => [
  {
    id: 'food',
    label: 'Comida',
    value: c.value?.food_rations ?? 0,
    max: 10,
    unit: '',
    iconPath: 'M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z M3 6h18 M16 10a4 4 0 01-8 0',
    depleted: (c.value?.food_rations ?? 0) === 0,
    danger: (c.value?.food_rations ?? 0) <= 2 && (c.value?.food_rations ?? 0) > 0,
    warning: (c.value?.food_rations ?? 0) <= 4 && (c.value?.food_rations ?? 0) > 0,
  },
  {
    id: 'gas',
    label: 'Gas (calor)',
    value: c.value?.gas_canisters ?? 0,
    max: 5,
    unit: '',
    iconPath: 'M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z',
    depleted: (c.value?.gas_canisters ?? 0) === 0,
    danger: (c.value?.gas_canisters ?? 0) === 0,
    warning: (c.value?.gas_canisters ?? 0) <= 1 && (c.value?.gas_canisters ?? 0) > 0,
  },
  {
    id: 'o2tanks',
    label: 'Tanques O₂',
    value: c.value?.oxygen_tanks ?? 0,
    max: 5,
    unit: '',
    iconPath: 'M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z',
    depleted: (c.value?.oxygen_tanks ?? 0) === 0,
    danger: (c.value?.oxygen_tanks ?? 0) === 0,
    warning: (c.value?.oxygen_tanks ?? 0) <= 1 && (c.value?.oxygen_tanks ?? 0) > 0,
  },
  {
    id: 'rope',
    label: 'Cuerda',
    value: c.value?.rope_sections ?? 0,
    max: 6,
    unit: ' m',
    iconPath: 'M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1',
    depleted: (c.value?.rope_sections ?? 0) === 0,
    danger: (c.value?.rope_sections ?? 0) === 0,
    warning: (c.value?.rope_sections ?? 0) <= 1 && (c.value?.rope_sections ?? 0) > 0,
  },
  {
    id: 'oxygen',
    label: 'Oxígeno',
    value: Math.round(c.value?.oxygen_pct ?? 0),
    max: 100,
    unit: '%',
    iconPath: 'M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z',
    depleted: (c.value?.oxygen_pct ?? 0) === 0,
    danger: (c.value?.oxygen_pct ?? 0) <= 20 && (c.value?.oxygen_pct ?? 0) > 0,
    warning: (c.value?.oxygen_pct ?? 0) <= 40 && (c.value?.oxygen_pct ?? 0) > 0,
  },
])

function toggleOxygen() {
  game.takeTurn('TOGGLE_OXYGEN')
}
</script>

<template>
  <div class="flex flex-col gap-3">
    <h2 class="text-xs uppercase tracking-[0.2em] text-ice/60 font-medium">Recursos</h2>

    <!-- Warnings Banner -->
    <TransitionGroup name="warn-fade" tag="div" class="flex flex-col gap-1">
      <div
        v-for="(w, i) in game.warnings"
        :key="i"
        class="px-3 py-1.5 rounded-lg border border-warning/30 bg-warning/8 text-[11px] text-warning flex items-center gap-2"
      >
        <svg class="w-3 h-3 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
          <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
          <line x1="12" y1="9" x2="12" y2="13" />
          <line x1="12" y1="17" x2="12.01" y2="17" />
        </svg>
        <span>{{ w }}</span>
      </div>
    </TransitionGroup>

    <div class="grid grid-cols-2 gap-2">
      <div
        v-for="res in resources"
        :key="res.id"
        class="relative flex flex-col gap-1.5 px-3 py-3 rounded-xl border transition-all duration-300"
        :class="[
          res.depleted
            ? 'opacity-40 border-white/5 bg-white/[0.01]'
            : res.danger
              ? 'border-danger/50 bg-danger/10 shadow-[0_0_12px_rgba(192,57,43,0.15)]'
              : res.warning
                ? 'border-warning/40 bg-warning/8'
                : 'border-white/8 bg-white/[0.02]',
        ]"
      >
        <!-- AGOTADO badge -->
        <span
          v-if="res.depleted"
          class="absolute top-2 right-2 px-1.5 py-0.5 rounded text-[8px] font-bold uppercase tracking-wider bg-danger/20 border border-danger/30 text-danger"
        >
          AGOTADO
        </span>

        <!-- Pulse dot when critical (only if not depleted) -->
        <span
          v-if="res.danger && !res.depleted"
          class="absolute top-2 right-2 w-1.5 h-1.5 rounded-full bg-danger animate-pulse"
        />

        <!-- Icon + label row -->
        <div class="flex items-center gap-2">
          <svg class="w-4 h-4" :class="res.depleted ? 'text-ice/20' : res.danger ? 'text-danger' : res.warning ? 'text-warning' : 'text-ice/60'" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
            <path :d="res.iconPath" />
          </svg>
          <span
            class="text-xs font-medium"
            :class="
              res.depleted ? 'text-ice/25' : res.danger ? 'text-danger' : res.warning ? 'text-warning' : 'text-ice/60'
            "
          >
            {{ res.label }}
          </span>
        </div>

        <!-- Value -->
        <span
          class="text-2xl font-mono font-bold leading-none"
          :class="
            res.depleted ? 'text-ice/20' : res.danger ? 'text-danger' : res.warning ? 'text-warning' : 'text-snow'
          "
        >
          {{ res.value }}<span class="text-sm font-normal opacity-60">{{ res.unit }}</span>
        </span>

        <!-- Mini progress bar -->
        <div class="h-1 w-full rounded-full bg-white/10 overflow-hidden">
          <div
            class="h-full rounded-full transition-all duration-500"
            :class="
              res.depleted ? 'bg-white/5' : res.danger ? 'bg-danger' : res.warning ? 'bg-warning' : 'bg-glacier/60'
            "
            :style="{ width: `${Math.min(100, (res.value / res.max) * 100)}%` }"
          />
        </div>

        <!-- Oxygen Valve Toggle Button (Only for oxygen card) -->
        <div v-if="res.id === 'oxygen'" class="mt-2.5 flex items-center justify-between gap-2 border-t border-white/5 pt-2.5">
          <span class="text-[9px] uppercase tracking-wider text-ice/40 font-medium">Válvula</span>
          <button 
            @click.stop="toggleOxygen"
            class="flex items-center gap-1.5 px-2.5 py-1 rounded text-[10px] font-bold border transition-all duration-300 active:scale-95"
            :class="[
              game.isLoading || (c?.oxygen_pct ?? 0) === 0
                ? 'opacity-30 cursor-not-allowed border-white/5 bg-white/[0.02] text-ice/20'
                : c?.oxygen_valve_open 
                  ? 'border-success/40 bg-success/10 text-success hover:bg-success/15 shadow-[0_0_10px_rgba(46,204,113,0.1)] cursor-pointer' 
                  : 'border-white/10 bg-white/5 text-ice/50 hover:bg-white/10 cursor-pointer',
            ]"
            :disabled="game.isLoading || (c?.oxygen_pct ?? 0) === 0"
            :title="(c?.oxygen_pct ?? 0) === 0 ? 'Sin oxígeno disponible' : ''"
          >
            <span class="w-1.5 h-1.5 rounded-full" :class="(c?.oxygen_pct ?? 0) === 0 ? 'bg-ice/20' : c?.oxygen_valve_open ? 'bg-success animate-pulse' : 'bg-ice/30'" />
            {{ c?.oxygen_valve_open ? 'ABIERTA' : 'CERRADA' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.warn-fade-enter-active { transition: all 0.3s ease-out; }
.warn-fade-leave-active { transition: all 0.3s ease-in; }
.warn-fade-enter-from,
.warn-fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
.warn-fade-move { transition: transform 0.3s ease; }
</style>
