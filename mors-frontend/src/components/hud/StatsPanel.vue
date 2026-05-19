<script setup lang="ts">
import StatBar from '@/components/shared/StatBar.vue'
import { useGameStore } from '@/stores/gameStore'

const game = useGameStore()
</script>

<template>
  <div class="flex flex-col gap-4">
    <h2 class="text-xs uppercase tracking-[0.2em] text-ice/60 font-medium">Vitales</h2>
    
    <div class="space-y-3">
      <StatBar
        label="HP"
        :value="game.state?.player.hp ?? 100"
        color="bg-danger"
        glow-class="stat-bar-glow-danger"
      />
      <StatBar
        label="Stamina"
        :value="game.state?.player.stamina ?? 100"
        color="bg-warning"
        glow-class="stat-bar-glow-warning"
      />
      <StatBar
        label="Temp"
        :value="game.state?.player.body_temp ?? 37"
        :min="30"
        :max="42"
        :optimal="37"
        color="bg-frost"
        unit="°C"
        glow-class="stat-bar-glow-glacier"
      />
      <StatBar
        label="Voluntad"
        :value="game.state?.player.willpower ?? 100"
        color="bg-ice"
      />
    </div>
  </div>
</template>
