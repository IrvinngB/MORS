<script setup lang="ts">
import { computed } from 'vue'
import { useUiStore } from '@/stores/uiStore'

const ui = useUiStore()

const borderColor = computed(() => {
  switch (ui.eventBannerType) {
    case 'danger':  return 'border-danger/50 bg-danger/10'
    case 'success': return 'border-success/50 bg-success/10'
    case 'info':    return 'border-glacier/30 bg-glacier/5'
    default:        return 'border-warning/40 bg-warning/8'
  }
})

const textColor = computed(() => {
  switch (ui.eventBannerType) {
    case 'danger':  return 'text-danger'
    case 'success': return 'text-success'
    case 'info':    return 'text-glacier'
    default:        return 'text-warning'
  }
})

const iconPath = computed(() => {
  switch (ui.eventBannerType) {
    case 'danger':
      // Warning triangle
      return 'M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z'
    case 'success':
      // Star / second wind
      return 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z'
    case 'info':
      // Eye / vision
      return 'M15 12a3 3 0 11-6 0 3 3 0 016 0zM2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z'
    default:
      // Wind / exclamation
      return 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
  }
})
</script>

<template>
  <Transition
    enter-active-class="transition-all duration-400 ease-out"
    enter-from-class="-translate-y-4 opacity-0 scale-95"
    enter-to-class="translate-y-0 opacity-100 scale-100"
    leave-active-class="transition-all duration-300 ease-in"
    leave-from-class="translate-y-0 opacity-100 scale-100"
    leave-to-class="-translate-y-4 opacity-0 scale-95"
  >
    <div
      v-if="ui.showEventBanner"
      class="fixed top-16 left-1/2 -translate-x-1/2 z-50 max-w-md w-full mx-auto px-4"
    >
      <div
        class="glass-strong rounded-xl px-5 py-4 shadow-2xl border flex items-start gap-3"
        :class="borderColor"
      >
        <!-- Icon -->
        <div class="flex-shrink-0 mt-0.5">
          <svg class="w-5 h-5" :class="textColor" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" :d="iconPath" />
          </svg>
        </div>
        <!-- Text -->
        <p class="text-sm leading-relaxed" :class="textColor">
          {{ ui.eventBannerText }}
        </p>
      </div>
    </div>
  </Transition>
</template>
