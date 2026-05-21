<script setup lang="ts">
import { ref, watch, computed } from 'vue'

export interface DeltaEntry {
  type: 'hp' | 'stamina' | 'temp' | 'willpower' | 'altitude' | 'oxygen' | 'route_secured'
  value: number
}

const props = withDefaults(defineProps<{
  delta?: number
  deltaType?: string
  deltas?: DeltaEntry[]
  unit?: string
  decimals?: number
  position?: 'top-right' | 'bottom-left' | 'bottom-right'
}>(), {
  delta: 0,
  deltaType: '',
  deltas: () => [],
  unit: '',
  decimals: 0,
  position: 'top-right',
})

const visible = ref(false)
const animKey = ref(0)

const entries = computed<DeltaEntry[]>(() => {
  if (props.deltas && props.deltas.length > 0) {
    return props.deltas.filter(d => d.value !== 0).slice(0, 3)
  }
  if (props.delta !== 0 && props.deltaType) {
    return [{ type: props.deltaType as DeltaEntry['type'], value: props.delta }]
  }
  return []
})

watch(entries, (newEntries) => {
  if (newEntries.length === 0) return
  visible.value = false
  requestAnimationFrame(() => {
    animKey.value++
    visible.value = true
    setTimeout(() => { visible.value = false }, 2200)
  })
})

const ICONS: Record<string, string> = {
  altitude: 'M12 2L4 22h16L12 2zm0 4l5.5 14h-11L12 6z',
  stamina: 'M13 2L3 14h8l-1 8 10-12h-8l1-8z',
  oxygen: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z',
  willpower: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z',
  hp: 'M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z',
  temp: 'M15 13V5c0-1.66-1.34-3-3-3S9 3.34 9 5v8c-1.21.91-2 2.37-2 4 0 2.76 2.24 5 5 5s5-2.24 5-5c0-1.63-.79-3.09-2-4zm-4-8c0-.55.45-1 1-1s1 .45 1 1h-1v1h1v2h-1v1h1v2h-2V5z',
  route_secured: 'M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1',
}

function getIcon(type: string): string {
  return ICONS[type] ?? ''
}

function getColor(type: string, value: number): string {
  if (value === 0) return 'text-ice/40'
  const positive = value > 0
  switch (type) {
    case 'altitude':
      return positive ? 'text-success' : 'text-danger'
    case 'stamina':
      return positive ? 'text-success' : value < -20 ? 'text-danger' : 'text-warning'
    case 'oxygen':
      return positive ? 'text-glacier' : 'text-ice'
    case 'willpower':
      return positive ? 'text-success' : 'text-purple-400'
    case 'hp':
      return positive ? 'text-success' : 'text-danger'
    case 'temp':
      return positive ? 'text-warning' : 'text-ice'
    case 'route_secured':
      return positive ? 'text-glacier' : 'text-danger'
    default:
      return positive ? 'text-success' : 'text-danger'
  }
}

function formatValue(type: string, value: number, decimals: number, unit: string): string {
  const sign = value > 0 ? '+' : ''
  const num = value.toFixed(decimals)
  switch (type) {
    case 'altitude':
      return `${sign}${num}m`
    case 'oxygen':
      return `${sign}${num}% O₂`
    case 'stamina':
      return `${sign}${num} stamina`
    case 'willpower':
      return `${sign}${num} WP`
    case 'hp':
      return `${sign}${num} HP`
    case 'temp':
      return `${sign}${num}°C`
    default:
      return `${sign}${num}${unit}`
  }
}

const positionClasses = computed(() => {
  switch (props.position) {
    case 'bottom-left':
      return 'delta-bottom-left'
    case 'bottom-right':
      return 'delta-bottom-right'
    default:
      return 'delta-top-right'
  }
})
</script>

<template>
  <Transition name="delta-float">
    <div
      v-if="visible && entries.length > 0"
      :key="animKey"
      class="delta-stack pointer-events-none select-none"
      :class="positionClasses"
    >
      <div
        v-for="(entry, idx) in entries"
        :key="entry.type + '-' + idx"
        class="delta-entry flex items-center gap-0.5 text-xs font-mono font-bold"
        :class="getColor(entry.type, entry.value)"
      >
        <svg v-if="getIcon(entry.type)" class="w-3 h-3 inline-block shrink-0" fill="currentColor" viewBox="0 0 24 24">
          <path :d="getIcon(entry.type)" />
        </svg>
        <span>{{ formatValue(entry.type, entry.value, decimals, unit) }}</span>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.delta-stack {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.delta-entry {
  display: inline-flex;
  align-items: center;
  white-space: nowrap;
}

.delta-top-right .delta-entry {
  animation: delta-rise 2.2s ease-out forwards;
}

.delta-bottom-left .delta-entry {
  animation: delta-fall-left 2.2s ease-out forwards;
}

.delta-bottom-right .delta-entry {
  animation: delta-fall-right 2.2s ease-out forwards;
}

.delta-float-enter-active .delta-entry {
  animation-duration: 2.2s;
}

.delta-float-leave-active {
  transition: opacity 0.2s ease;
}

.delta-float-leave-to {
  opacity: 0;
}

@keyframes delta-rise {
  0%   { opacity: 0; transform: translateY(0px); }
  15%  { opacity: 1; transform: translateY(-4px); }
  70%  { opacity: 1; transform: translateY(-10px); }
  100% { opacity: 0; transform: translateY(-18px); }
}

@keyframes delta-fall-left {
  0%   { opacity: 0; transform: translateY(0px) translateX(0px); }
  15%  { opacity: 1; transform: translateY(4px) translateX(-2px); }
  70%  { opacity: 1; transform: translateY(10px) translateX(-4px); }
  100% { opacity: 0; transform: translateY(18px) translateX(-6px); }
}

@keyframes delta-fall-right {
  0%   { opacity: 0; transform: translateY(0px) translateX(0px); }
  15%  { opacity: 1; transform: translateY(4px) translateX(2px); }
  70%  { opacity: 1; transform: translateY(10px) translateX(4px); }
  100% { opacity: 0; transform: translateY(18px) translateX(6px); }
}
</style>
