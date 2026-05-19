<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  label: string
  value: number
  min?: number
  max?: number
  optimal?: number
  color?: string
  unit?: string
  glowClass?: string
}>(), {
  min: 0,
  max: 100,
  optimal: undefined,
  color: 'bg-glacier',
  unit: '',
  glowClass: '',
})

const pct = computed(() => {
  return Math.min(100, Math.max(0, ((props.value - props.min) / (props.max - props.min)) * 100))
})

const barColor = computed(() => {
  if (props.optimal !== undefined) {
    const dist = Math.abs(props.value - props.optimal)
    if (dist <= 2) return 'bg-success'
    if (dist <= 5) return 'bg-warning'
    return 'bg-danger'
  }
  return props.color
})

const showGlow = computed(() => {
  if (props.optimal !== undefined) {
    const dist = Math.abs(props.value - props.optimal)
    return dist <= 2
  }
  return false
})
</script>

<template>
  <div class="flex items-center gap-3">
    <span class="text-xs text-ice/60 w-16 font-medium">{{ label }}</span>
    <div class="flex-1 h-2.5 bg-abyss/60 rounded-full overflow-hidden relative">
      <div
        class="h-full rounded-full transition-all duration-700 ease-out relative"
        :class="[barColor, showGlow ? glowClass : '']"
        :style="{ width: `${pct}%` }"
      />
    </div>
    <span class="text-xs text-snow font-mono w-14 text-right font-medium">
      {{ value.toFixed(unit === '°C' ? 1 : 0) }}{{ unit }}
    </span>
  </div>
</template>
