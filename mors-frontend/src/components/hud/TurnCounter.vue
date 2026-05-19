<script setup lang="ts">
import { useGameStore } from '@/stores/gameStore'

const game = useGameStore()
</script>

<template>
  <div class="flex flex-col items-center">
    <h2 class="text-xs uppercase tracking-[0.2em] text-ice/60 font-medium mb-2">Hora</h2>
    <div class="text-center">
      <p class="text-2xl font-bold font-mono text-snow">
        {{ game.turn }}
      </p>
      <p class="text-xs text-ice/50 mt-1 uppercase tracking-wider">
        {{ game.isNight ? 'Noche' : 'Día' }}
      </p>
      <div class="mt-2 w-8 h-8 mx-auto rounded-full border border-snow/20 flex items-center justify-center">
        <span class="text-sm">{{ game.isNight ? '☽' : '☀' }}</span>
      </div>
    </div>
  </div>
</template>
