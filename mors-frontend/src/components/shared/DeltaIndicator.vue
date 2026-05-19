<script setup lang="ts">
import { ref, watch, computed } from 'vue'

const props = withDefaults(defineProps<{
  delta: number
  unit?: string
  decimals?: number
}>(), {
  unit: '',
  decimals: 0,
})

const visible = ref(false)
const animKey = ref(0)

watch(() => props.delta, (newDelta) => {
  if (newDelta === 0) return
  visible.value = false
  requestAnimationFrame(() => {
    animKey.value++
    visible.value = true
    setTimeout(() => { visible.value = false }, 2200)
  })
})

const isPositive = computed(() => props.delta > 0)
const formatted = computed(() => {
  const sign = props.delta > 0 ? '+' : ''
  return `${sign}${props.delta.toFixed(props.decimals)}${props.unit}`
})
</script>

<template>
  <Transition name="delta-float">
    <span
      v-if="visible && delta !== 0"
      :key="animKey"
      class="delta-indicator text-xs font-mono font-bold pointer-events-none select-none"
      :class="isPositive ? 'text-success' : 'text-danger'"
    >
      {{ formatted }}
    </span>
  </Transition>
</template>

<style scoped>
.delta-indicator {
  display: inline-block;
}

.delta-float-enter-active {
  animation: delta-rise 2.2s ease-out forwards;
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
</style>
