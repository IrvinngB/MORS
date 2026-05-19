<script setup lang="ts">
import { ref, watch } from 'vue'

const props = withDefaults(defineProps<{
  value: number
  duration?: number
}>(), {
  duration: 600,
})

const display = ref(props.value)
let raf: number | null = null

watch(
  () => props.value,
  (newVal, oldVal) => {
    if (raf) cancelAnimationFrame(raf)
    const start = oldVal
    const startTime = performance.now()

    function step(now: number) {
      const elapsed = now - startTime
      const progress = Math.min(elapsed / props.duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      display.value = start + (newVal - start) * eased
      if (progress < 1) raf = requestAnimationFrame(step)
    }
    raf = requestAnimationFrame(step)
  }
)
</script>

<template>
  <span
    class="font-mono font-medium transition-colors duration-300"
    :class="value > 0 ? 'text-success' : value < 0 ? 'text-danger' : 'text-ice/40'"
  >
    {{ value > 0 ? '+' : '' }}{{ display.toFixed(1) }}
  </span>
</template>
