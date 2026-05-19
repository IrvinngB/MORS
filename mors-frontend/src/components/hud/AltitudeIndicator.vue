<script setup lang="ts">
import { computed } from 'vue'
import { useGameStore } from '@/stores/gameStore'

const game = useGameStore()

const progress = computed(() => {
  const alt = game.altitude
  const min = 5200
  const max = 8611
  return Math.min(100, ((alt - min) / (max - min)) * 100)
})

const deathZoneStart = computed(() => {
  const min = 5200
  const max = 8611
  return ((8000 - min) / (max - min)) * 100
})
</script>

<template>
  <div class="flex flex-col items-center">
    <h2 class="text-xs uppercase tracking-[0.2em] text-ice/60 font-medium mb-4">Altitud</h2>
    
    <div class="relative h-56 w-12 bg-abyss/50 rounded-lg overflow-hidden border border-white/10">
      <!-- Death zone marker -->
      <div
        class="absolute left-0 right-0 bg-gradient-to-t from-death-zone/40 to-death-zone/10"
        :style="{ bottom: `${deathZoneStart}%`, height: `${100 - deathZoneStart}%` }"
      />
      
      <!-- Progress bar -->
      <div
        class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-glacier to-frost transition-all duration-700 ease-out"
        :style="{ height: `${progress}%` }"
      />
      
      <!-- Current position marker -->
      <div
        class="absolute -left-1 w-14 h-0.5 bg-snow shadow-[0_0_8px_rgba(255,255,255,0.8)] transition-all duration-700"
        :style="{ bottom: `${progress}%` }"
      />
      
      <!-- Summit marker -->
      <div class="absolute top-0 left-0 right-0 h-px bg-snow/30" />
    </div>
    
    <div class="mt-4 text-center">
      <p class="text-xl font-bold font-mono text-snow">
        {{ game.altitude.toFixed(0) }}<span class="text-sm text-ice/60 ml-1">m</span>
      </p>
      <p class="text-[10px] text-death-zone/80 mt-1 uppercase tracking-wider">
        Zona de Muerte: 8000m
      </p>
    </div>
  </div>
</template>
