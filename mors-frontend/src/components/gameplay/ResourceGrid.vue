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
    danger: (c.value?.food_rations ?? 0) <= 2,
    warning: (c.value?.food_rations ?? 0) <= 4,
  },
  {
    id: 'gas',
    label: 'Gas',
    value: c.value?.gas_canisters ?? 0,
    max: 5,
    unit: '',
    iconPath: 'M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z',
    danger: (c.value?.gas_canisters ?? 0) === 0,
    warning: (c.value?.gas_canisters ?? 0) <= 1,
  },
  {
    id: 'rope',
    label: 'Cuerda',
    value: c.value?.rope_sections ?? 0,
    max: 6,
    unit: ' m',
    iconPath: 'M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1',
    danger: (c.value?.rope_sections ?? 0) === 0,
    warning: (c.value?.rope_sections ?? 0) <= 1,
  },
  {
    id: 'oxygen',
    label: 'Oxígeno',
    value: Math.round(c.value?.oxygen_pct ?? 0),
    max: 100,
    unit: '%',
    iconPath: 'M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z',
    danger: (c.value?.oxygen_pct ?? 0) <= 20,
    warning: (c.value?.oxygen_pct ?? 0) <= 40,
  },
])
</script>

<template>
  <div class="flex flex-col gap-3">
    <h2 class="text-xs uppercase tracking-[0.2em] text-ice/60 font-medium">Recursos</h2>

    <div class="grid grid-cols-2 gap-2">
      <div
        v-for="res in resources"
        :key="res.id"
        class="relative flex flex-col gap-1.5 px-3 py-3 rounded-xl border transition-all duration-300"
        :class="
          res.danger
            ? 'border-danger/50 bg-danger/10 shadow-[0_0_12px_rgba(192,57,43,0.15)]'
            : res.warning
              ? 'border-warning/40 bg-warning/8'
              : 'border-white/8 bg-white/[0.02]'
        "
      >
        <!-- Pulse dot when critical -->
        <span
          v-if="res.danger"
          class="absolute top-2 right-2 w-1.5 h-1.5 rounded-full bg-danger animate-pulse"
        />

        <!-- Icon + label row -->
        <div class="flex items-center gap-2">
          <svg class="w-4 h-4" :class="res.danger ? 'text-danger' : res.warning ? 'text-warning' : 'text-ice/60'" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
            <path :d="res.iconPath" />
          </svg>
          <span
            class="text-xs font-medium"
            :class="
              res.danger ? 'text-danger' : res.warning ? 'text-warning' : 'text-ice/60'
            "
          >
            {{ res.label }}
          </span>
        </div>

        <!-- Value -->
        <span
          class="text-2xl font-mono font-bold leading-none"
          :class="
            res.danger ? 'text-danger' : res.warning ? 'text-warning' : 'text-snow'
          "
        >
          {{ res.value }}<span class="text-sm font-normal opacity-60">{{ res.unit }}</span>
        </span>

        <!-- Mini progress bar -->
        <div class="h-1 w-full rounded-full bg-white/10 overflow-hidden">
          <div
            class="h-full rounded-full transition-all duration-500"
            :class="
              res.danger ? 'bg-danger' : res.warning ? 'bg-warning' : 'bg-glacier/60'
            "
            :style="{ width: `${Math.min(100, (res.value / res.max) * 100)}%` }"
          />
        </div>
      </div>
    </div>
  </div>
</template>
