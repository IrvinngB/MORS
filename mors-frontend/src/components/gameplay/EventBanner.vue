<script setup lang="ts">
import { useUiStore } from '@/stores/uiStore'

const ui = useUiStore()
</script>

<template>
  <Transition
    enter-active-class="transition-all duration-500 ease-out"
    enter-from-class="translate-y-full opacity-0"
    enter-to-class="translate-y-0 opacity-100"
    leave-active-class="transition-all duration-300 ease-in"
    leave-from-class="translate-y-0 opacity-100"
    leave-to-class="translate-y-full opacity-0"
  >
    <div
      v-if="ui.showEventBanner"
      class="fixed top-20 left-1/2 -translate-x-1/2 glass-strong px-6 py-3 rounded-lg shadow-2xl z-50 border border-warning/30"
    >
      <p class="text-sm font-medium text-warning">{{ ui.eventBannerText }}</p>
    </div>
  </Transition>
</template>
