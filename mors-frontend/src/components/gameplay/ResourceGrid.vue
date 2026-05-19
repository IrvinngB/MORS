<script setup lang="ts">
import { useGameStore } from '@/stores/gameStore'

const game = useGameStore()
</script>

<template>
  <div class="flex flex-col gap-3">
    <h2 class="text-xs uppercase tracking-[0.2em] text-ice/60 font-medium">Recursos</h2>
    
    <div class="grid grid-cols-2 gap-3">
      <div class="flex items-center justify-between px-3 py-2 rounded-lg bg-abyss/40 border border-white/5">
        <span class="text-xs text-ice/50">Comida</span>
        <span class="text-sm font-mono font-medium text-snow">{{ game.state?.consumables.food_rations ?? 0 }}</span>
      </div>
      <div class="flex items-center justify-between px-3 py-2 rounded-lg bg-abyss/40 border border-white/5">
        <span class="text-xs text-ice/50">Gas</span>
        <span class="text-sm font-mono font-medium text-snow">{{ game.state?.consumables.gas_canisters ?? 0 }}</span>
      </div>
      <div class="flex items-center justify-between px-3 py-2 rounded-lg bg-abyss/40 border border-white/5">
        <span class="text-xs text-ice/50">Cuerda</span>
        <span class="text-sm font-mono font-medium text-snow">{{ game.state?.consumables.rope_sections ?? 0 }}</span>
      </div>
      <div class="flex items-center justify-between px-3 py-2 rounded-lg bg-abyss/40 border border-white/5">
        <span class="text-xs text-ice/50">O₂</span>
        <span class="text-sm font-mono font-medium text-snow">{{ game.state?.consumables.oxygen_pct ?? 0 }}%</span>
      </div>
    </div>
  </div>
</template>
