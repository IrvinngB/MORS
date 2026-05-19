<script setup lang="ts">
import { computed } from 'vue'
import { useGameStore } from '@/stores/gameStore'

const game = useGameStore()

const weatherLabel: Record<string, string> = {
  CLEAR: 'Despejado',
  CLOUDY: 'Nublado',
  WIND: 'Viento',
  STORM: 'Tormenta',
  WHITEOUT: 'Ventisca',
}

const reliabilityColor = computed(() => {
  const r = game.state?.forecast_reliability ?? 1
  if (r > 0.8) return 'text-success'
  if (r > 0.5) return 'text-warning'
  return 'text-danger'
})

const weatherIcon: Record<string, string> = {
  CLEAR: '○',
  CLOUDY: '◐',
  WIND: '≋',
  STORM: '◈',
  WHITEOUT: '◉',
}
</script>

<template>
  <div class="flex flex-col gap-3">
    <h2 class="text-xs uppercase tracking-[0.2em] text-ice/60 font-medium">Clima</h2>
    
    <div class="flex items-center gap-3">
      <span class="text-3xl text-glacier/80">{{ weatherIcon[game.state?.weather ?? 'CLEAR'] }}</span>
      <div>
        <p class="text-snow font-medium">{{ weatherLabel[game.state?.weather ?? 'CLEAR'] }}</p>
        <p class="text-ice/50 text-xs">Pronóstico: {{ weatherLabel[game.state?.weather_forecast ?? 'CLEAR'] }}</p>
      </div>
    </div>
    
    <div class="flex items-center justify-between text-xs">
      <span class="text-ice/50">Fiabilidad</span>
      <span class="font-mono font-medium" :class="reliabilityColor">
        {{ ((game.state?.forecast_reliability ?? 1) * 100).toFixed(0) }}%
      </span>
    </div>
    
    <!-- Reliability bar -->
    <div class="h-1 bg-abyss/50 rounded-full overflow-hidden">
      <div 
        class="h-full rounded-full transition-all duration-500"
        :class="reliabilityColor.replace('text-', 'bg-')"
        :style="{ width: `${(game.state?.forecast_reliability ?? 1) * 100}%` }"
      />
    </div>
  </div>
</template>
