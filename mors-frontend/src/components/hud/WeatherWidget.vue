<script setup lang="ts">
import { computed, ref, watch } from 'vue'
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

// Detección de cambios de clima repentinos e imprevistos
const previousForecast = ref<string | null>(null)
const suddenChange = ref(false)

watch(() => game.state?.turn, (newTurn) => {
  if (newTurn && game.state) {
    // Si el clima real difiere del pronóstico que se dio en el turno anterior
    if (previousForecast.value && game.state.weather !== previousForecast.value) {
      suddenChange.value = true
      setTimeout(() => {
        suddenChange.value = false
      }, 5000)
    }
    // Guardamos el pronóstico actual para comparar en el siguiente turno
    previousForecast.value = game.state.weather_forecast
  }
}, { immediate: true })
</script>

<template>
  <div class="flex flex-col gap-3">
    <h2 class="text-xs uppercase tracking-[0.2em] text-ice/60 font-medium">Clima</h2>
    
    <div class="flex items-center gap-3">
      <!-- Iconos Climatológicos Premium SVG -->
      <div class="flex items-center justify-center w-10 h-10 rounded-xl bg-white/[0.02] border border-white/5 shadow-inner">
        <!-- CLEAR (Sol giratorio sutil) -->
        <svg v-if="game.state?.weather === 'CLEAR'" class="w-6 h-6 text-warning/80 animate-spin" style="animation-duration: 20s" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="5" />
          <path d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72l1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
        </svg>

        <!-- CLOUDY (Nube estática minimalista) -->
        <svg v-else-if="game.state?.weather === 'CLOUDY'" class="w-6 h-6 text-ice/50" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
        </svg>

        <!-- WIND (Viento ondulado dinámico) -->
        <svg v-else-if="game.state?.weather === 'WIND'" class="w-6 h-6 text-glacier/80 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path d="M2 8h16.5a2.5 2.5 0 000-5M2 12h19.5a2.5 2.5 0 010 5M2 16h14.5a2.5 2.5 0 000-5" />
        </svg>

        <!-- STORM (Tormenta, nube de peligro con rayo) -->
        <svg v-else-if="game.state?.weather === 'STORM'" class="w-6 h-6 text-danger/80 animate-bounce" style="animation-duration: 2.5s" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path d="M19 16.9A5 5 0 0018 7h-1.26a8 8 0 10-11.62 8.58M13 11l-4 6h6l-3 5" />
        </svg>

        <!-- WHITEOUT (Ventisca violenta giratoria rápida) -->
        <svg v-else-if="game.state?.weather === 'WHITEOUT'" class="w-6 h-6 text-snow animate-spin" style="animation-duration: 6s" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path d="M12 3v3m0 12v3M4.93 4.93l2.12 2.12m9.9 9.9l2.12 2.12M3 12h3m12 0h3M4.93 19.07l2.12-2.12m9.9-9.9l2.12-2.12M12 12h.01" />
        </svg>
      </div>
      
      <div>
        <p class="text-snow font-medium">{{ weatherLabel[game.state?.weather ?? 'CLEAR'] }}</p>
        <p class="text-ice/50 text-xs">Pronóstico: {{ weatherLabel[game.state?.weather_forecast ?? 'CLEAR'] }}</p>
      </div>
    </div>

    <!-- Alerta de Cambio de Clima Imprevisto -->
    <div 
      v-if="suddenChange" 
      class="text-[10px] text-danger bg-danger/5 border border-danger/20 rounded-lg px-2.5 py-1.5 flex items-center gap-1.5 animate-pulse"
    >
      <span class="w-1.5 h-1.5 rounded-full bg-danger animate-ping" />
      <span class="font-bold tracking-wider uppercase">¡Cambio Climático Imprevisto!</span>
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
