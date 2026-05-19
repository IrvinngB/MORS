import { ref, watch } from 'vue'
import type { Ref } from 'vue'

export function useAnimatedStats<T extends Record<string, number>>(
  target: Ref<T | null>,
  keys: (keyof T)[],
  duration = 600
) {
  const displayValues = ref<Record<string, number>>({}) as Ref<Record<string, number>>

  watch(
    () => target.value,
    (newVal) => {
      if (!newVal) return
      for (const key of keys) {
        const current = displayValues.value[key as string] ?? newVal[key]
        const targetVal = newVal[key]
        if (current === targetVal) continue

        const startTime = performance.now()
        const from = current

        function step(now: number) {
          const elapsed = now - startTime
          const progress = Math.min(elapsed / duration, 1)
          const eased = 1 - Math.pow(1 - progress, 3)
          displayValues.value = { ...displayValues.value, [key]: (from ?? 0) + ((targetVal ?? 0) - (from ?? 0)) * eased }
          if (progress < 1) requestAnimationFrame(step)
        }
        requestAnimationFrame(step)
      }
    },
    { immediate: true }
  )

  return displayValues
}