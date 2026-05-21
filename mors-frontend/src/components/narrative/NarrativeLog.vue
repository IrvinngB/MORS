<script setup lang="ts">
import { computed, ref, watch, onUnmounted } from 'vue'
import { useGameStore } from '@/stores/gameStore'

const game = useGameStore()

const visibleCharCount = ref(0)
let typewriterTimer: ReturnType<typeof setInterval> | null = null
let isTypingComplete = ref(true)

const logEntries = computed(() => {
  const log = game.state?.narrative_log ?? []
  return log
    .slice(-25)
    .map((text, i, arr) => ({
      text,
      isLatest: i === arr.length - 1,
      turnNum: (game.turn ?? 0) - (arr.length - 1 - i),
    }))
    .reverse()
})

const latestEntry = computed(() => {
  const entries = logEntries.value
  return entries.length > 0 ? entries[entries.length - 1] : null
})

const latestText = computed(() => latestEntry.value?.text ?? '')

const typewriterSpeed = computed(() => {
  const wp = game.state?.player?.willpower ?? 100
  if (wp < 15) return 60
  if (wp < 30) return 45
  return 25
})

const altitudeTier = computed(() => {
  const alt = game.altitude
  if (alt >= 8000) return 'death_zone'
  if (alt >= 7000) return 'high'
  if (alt >= 6000) return 'mid'
  return 'low'
})

function getBorderClass(tier: string, isLatest: boolean): string {
  if (!isLatest) return 'border-white/8 opacity-30'
  switch (tier) {
    case 'death_zone': return 'border-danger animate-pulse'
    case 'high': return 'border-danger/70'
    case 'mid': return 'border-warning'
    case 'low': default: return 'border-glacier'
  }
}

function getBgClass(tier: string, isLatest: boolean): string {
  if (!isLatest) return ''
  switch (tier) {
    case 'death_zone': return 'bg-danger/[0.03]'
    case 'high': return 'bg-danger/[0.02]'
    case 'mid': return 'bg-warning/[0.02]'
    case 'low': default: return 'bg-glacier/[0.03]'
  }
}

function getRoundedClass(tier: string, isLatest: boolean): string {
  if (!isLatest) return ''
  return 'rounded-r-lg'
}

function getTextColorClass(isLatest: boolean): string {
  if (!isLatest) return 'text-ice/50'
  const wp = game.state?.player?.willpower ?? 100
  if (wp < 15) return 'text-danger/70 text-shadow-danger'
  if (wp < 30) return 'text-ice/70'
  return 'text-snow/90'
}

function getDisplayedText(entry: { text: string; isLatest: boolean; turnNum: number }): string {
  if (!entry.isLatest || isTypingComplete.value) return entry.text
  return entry.text.slice(0, visibleCharCount.value)
}

function startTypewriter(text: string) {
  stopTypewriter()
  if (!text) {
    isTypingComplete.value = true
    return
  }
  visibleCharCount.value = 0
  isTypingComplete.value = false

  typewriterTimer = setInterval(() => {
    visibleCharCount.value++
    if (visibleCharCount.value >= text.length) {
      stopTypewriter()
      isTypingComplete.value = true
    }
  }, typewriterSpeed.value)
}

function stopTypewriter() {
  if (typewriterTimer) {
    clearInterval(typewriterTimer)
    typewriterTimer = null
  }
}

watch(latestText, (newText) => {
  startTypewriter(newText ?? '')
}, { immediate: true })

onUnmounted(() => {
  stopTypewriter()
})

function formatTurn(turnNum: number): string {
  if (turnNum <= 0) return 'Inicio'
  const hour = (turnNum - 1) % 24
  const label = hour >= 12 ? 'Noche' : 'Día'
  return `T${turnNum} · ${label}`
}

function getTierLabel(tier: string): string {
  switch (tier) {
    case 'death_zone': return 'ZONA DE LA MUERTE'
    case 'high': return 'Altitud extrema'
    case 'mid': return 'Zona de transición'
    case 'low': default: return ''
  }
}
</script>

<template>
  <div class="flex flex-col h-full min-h-0">
    <h2 class="text-xs uppercase tracking-[0.2em] text-ice/60 font-medium mb-3 flex-shrink-0">
      Bitácora
    </h2>

    <div class="flex-1 overflow-y-auto pr-1 min-h-0">
      <TransitionGroup name="log-entry" tag="div" class="space-y-3">
        <div
          v-for="entry in logEntries"
          :key="entry.turnNum"
          class="narrative-entry border-l-2 pl-3 transition-all duration-300"
          :class="[
            getBorderClass(entry.isLatest ? altitudeTier : 'low', entry.isLatest),
            getBgClass(entry.isLatest ? altitudeTier : 'low', entry.isLatest),
            getRoundedClass(entry.isLatest ? altitudeTier : 'low', entry.isLatest),
          ]"
        >
          <div class="flex items-center gap-2 mb-1">
            <span
              class="text-[10px] font-mono block"
              :class="entry.isLatest ? 'text-glacier/60' : 'text-ice/25'"
            >
              {{ formatTurn(entry.turnNum) }}
            </span>
            <span
              v-if="entry.isLatest && altitudeTier !== 'low'"
              class="text-[9px] uppercase tracking-wider font-bold px-1.5 py-0.5 rounded"
              :class="
                altitudeTier === 'death_zone'
                  ? 'text-danger/80 bg-danger/10 animate-pulse'
                  : altitudeTier === 'high'
                    ? 'text-danger/60 bg-danger/5'
                    : 'text-warning/70 bg-warning/5'
              "
            >
              {{ getTierLabel(altitudeTier) }}
            </span>
          </div>

          <template v-if="entry.isLatest && latestEntry">
            <p
              class="text-sm leading-relaxed whitespace-pre-line"
              :class="getTextColorClass(entry.isLatest)"
            >
              <template v-if="isTypingComplete">
                <template v-for="(paragraph, pIdx) in latestEntry.text.split('\n\n')" :key="pIdx">
                  <span v-if="pIdx > 0" class="block mt-2"></span>
                  <span
                    v-if="pIdx > 0"
                    class="block text-xs italic text-ice/60 bg-warning/5 border-l-2 border-warning/40 pl-2 py-1 rounded-r"
                  >{{ paragraph }}</span>
                  <span v-else>{{ paragraph }}</span>
                </template>
              </template>
              <template v-else>
                {{ getDisplayedText(entry) }}
              </template>
            </p>
            <span v-if="!isTypingComplete" class="typing-cursor text-glacier/80 text-sm" />
          </template>
          <template v-else>
            <p
              class="text-sm leading-relaxed whitespace-pre-line"
              :class="getTextColorClass(entry.isLatest)"
            >
              {{ entry.text }}
            </p>
          </template>
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
  transition: all 0.4s ease-out;
}

.log-entry-enter-from {
  opacity: 0;
  transform: translateY(-8px);
}

.narrative-entry {
  padding-bottom: 2px;
}
</style>
