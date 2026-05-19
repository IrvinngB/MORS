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
  <div class="flex flex-col h-full min-h-0">
    <h2 class="text-xs uppercase tracking-[0.2em] text-ice/60 font-medium mb-3">Bitácora</h2>
    <div class="flex-1 overflow-y-auto space-y-3 pr-2">
      <p
        v-for="(entry, i) in logEntries"
        :key="i"
        class="text-sm text-ice/60 leading-relaxed border-l-2 border-white/10 pl-3"
        :class="{ 'text-snow font-medium border-glacier/50': i === logEntries.length - 1 }"
      >
        {{ entry }}
      </p>
      <p v-if="logEntries.length === 0" class="text-sm text-ice/30 italic">
        La expedición comienza...
      </p>
    </div>
  </div>
</template>
