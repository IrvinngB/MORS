<script setup lang="ts">
import { computed, ref, watch, nextTick } from 'vue'
import { useGameStore } from '@/stores/gameStore'

const game = useGameStore()
const scrollContainer = ref<HTMLElement | null>(null)

const logEntries = computed(() => {
  const log = game.state?.narrative_log ?? []
  // Show last 25 entries, each with an index for keying
  return log.slice(-25).map((text, i, arr) => ({
    text,
    isLatest: i === arr.length - 1,
    turnNum: (game.turn ?? 0) - (arr.length - 1 - i),
  }))
})

// Auto-scroll to bottom when new entries arrive
watch(
  () => logEntries.value.length,
  async () => {
    await nextTick()
    if (scrollContainer.value) {
      scrollContainer.value.scrollTop = scrollContainer.value.scrollHeight
    }
  }
)

function formatTurn(turnNum: number): string {
  if (turnNum <= 0) return 'Inicio'
  const hour = ((turnNum - 1) % 24)
  const isNight = hour >= 12
  const label = isNight ? 'Noche' : 'Día'
  return `T${turnNum} · ${label}`
}
</script>

<template>
  <div class="flex flex-col h-full min-h-0">
    <h2 class="text-xs uppercase tracking-[0.2em] text-ice/60 font-medium mb-3 flex-shrink-0">
      Bitácora
    </h2>

    <div
      ref="scrollContainer"
      class="flex-1 overflow-y-auto space-y-3 pr-1 min-h-0"
    >
      <TransitionGroup name="log-entry" tag="div" class="space-y-3">
        <div
          v-for="(entry, i) in logEntries"
          :key="entry.turnNum + '-' + i"
          class="narrative-entry border-l-2 pl-3 transition-all duration-300"
          :class="entry.isLatest
            ? 'border-glacier/50 bg-glacier/[0.03] rounded-r-lg py-1'
            : 'border-white/8'"
        >
          <!-- Turn timestamp -->
          <span
            class="text-[10px] font-mono mb-1 block"
            :class="entry.isLatest ? 'text-glacier/60' : 'text-ice/25'"
          >
            {{ formatTurn(entry.turnNum) }}
          </span>
          <!-- Narrative text -->
          <p
            class="text-sm leading-relaxed"
            :class="entry.isLatest ? 'text-snow/90' : 'text-ice/50'"
          >
            {{ entry.text }}
          </p>
        </div>
      </TransitionGroup>

      <p v-if="logEntries.length === 0" class="text-sm text-ice/30 italic pl-3">
        La expedición comienza en silencio.
      </p>
    </div>
  </div>
</template>

<style scoped>
.log-entry-enter-active {
  transition: all 0.5s ease-out;
}

.log-entry-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.narrative-entry {
  padding-bottom: 2px;
}
</style>
