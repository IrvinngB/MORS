<script setup lang="ts">
import { computed } from 'vue'
import { useGameStore } from '@/stores/gameStore'

const game = useGameStore()

const logEntries = computed(() => {
  const log = game.state?.narrative_log ?? []
  return log.slice(-20)
})
</script>

<template>
  <div class="flex-1 flex flex-col min-h-0">
    <h2 class="text-xs uppercase tracking-widest text-ice mb-2">Bitácora</h2>
    <div class="flex-1 overflow-y-auto bg-peak/30 rounded p-3 space-y-2">
      <p
        v-for="(entry, i) in logEntries"
        :key="i"
        class="text-sm text-snow/80 leading-relaxed"
        :class="{ 'text-snow font-medium': i === logEntries.length - 1 }"
      >
        {{ entry }}
      </p>
    </div>
  </div>
</template>