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
}>(), {
  min: 0,
  max: 100,
  optimal: undefined,
  color: 'bg-glacier',
  unit: '',
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
</script>

<template>
  <div class="flex items-center gap-2">
    <span class="text-xs text-ice w-10">{{ label }}</span>
    <div class="flex-1 h-2 bg-peak/50 rounded overflow-hidden">
      <div
        class="h-full transition-all duration-500 rounded"
        :class="barColor"
        :style="{ width: `${pct}%` }"
      />
    </div>
    <span class="text-xs text-snow font-mono w-12 text-right">
      {{ value.toFixed(unit === '°C' ? 1 : 0) }}{{ unit }}
    </span>
  </div>
</template>