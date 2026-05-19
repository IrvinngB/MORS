<script setup lang="ts">
import { useGameStore } from '@/stores/gameStore'

const game = useGameStore()
</script>

<template>
  <div class="grid grid-cols-2 gap-2 text-sm">
    <div class="flex justify-between">
      <span class="text-ice">Comida</span>
      <span class="text-snow font-mono">{{ game.state?.consumables.food_rations ?? 0 }}</span>
    </div>
    <div class="flex justify-between">
      <span class="text-ice">Gas</span>
      <span class="text-snow font-mono">{{ game.state?.consumables.gas_canisters ?? 0 }}</span>
    </div>
    <div class="flex justify-between">
      <span class="text-ice">Cuerda</span>
      <span class="text-snow font-mono">{{ game.state?.consumables.rope_sections ?? 0 }}</span>
    </div>
    <div class="flex justify-between">
      <span class="text-ice">O₂</span>
      <span class="text-snow font-mono">{{ game.state?.consumables.oxygen_pct ?? 0 }}%</span>
    </div>
  </div>
</template>