<script setup lang="ts">
import { computed, toRef } from 'vue'
import StatBar from '@/components/shared/StatBar.vue'
import DeltaIndicator from '@/components/shared/DeltaIndicator.vue'
import { useGameStore } from '@/stores/gameStore'
import { useAnimatedStats } from '@/composables/useAnimatedStats'

const game = useGameStore()

const playerRef = computed(() => game.state?.player ?? null)

const animatedValues = useAnimatedStats(playerRef, ['hp', 'stamina', 'body_temp', 'willpower'])

const hpVal     = computed(() => animatedValues.value.hp     ?? game.state?.player.hp     ?? 100)
const staminaVal = computed(() => animatedValues.value.stamina ?? game.state?.player.stamina ?? 100)
const tempVal   = computed(() => animatedValues.value.body_temp ?? game.state?.player.body_temp ?? 37)
const wpVal     = computed(() => animatedValues.value.willpower ?? game.state?.player.willpower ?? 100)
</script>

<template>
  <div class="flex flex-col gap-4">
    <h2 class="text-xs uppercase tracking-[0.2em] text-ice/60 font-medium">Vitales</h2>

    <div class="space-y-3">
      <!-- HP -->
      <div class="relative">
        <StatBar
          label="HP"
          :value="hpVal"
          color="bg-danger"
          glow-class="stat-bar-glow-danger"
        />
        <div class="absolute right-0 top-0 -mt-4">
          <DeltaIndicator :delta="game.deltas?.hp_delta ?? 0" :decimals="1" />
        </div>
      </div>

      <!-- Stamina -->
      <div class="relative">
        <StatBar
          label="Stamina"
          :value="staminaVal"
          color="bg-warning"
          glow-class="stat-bar-glow-warning"
        />
        <div class="absolute right-0 top-0 -mt-4">
          <DeltaIndicator :delta="game.deltas?.stamina_delta ?? 0" :decimals="1" />
        </div>
      </div>

      <!-- Temperature -->
      <div class="relative">
        <StatBar
          label="Temp"
          :value="tempVal"
          :min="30"
          :max="42"
          :optimal="37"
          color="bg-frost"
          unit="°C"
          glow-class="stat-bar-glow-glacier"
        />
        <div class="absolute right-0 top-0 -mt-4">
          <DeltaIndicator :delta="game.deltas?.temp_delta ?? 0" :decimals="2" unit="°C" />
        </div>
      </div>

      <!-- Willpower -->
      <div class="relative">
        <StatBar
          label="Voluntad"
          :value="wpVal"
          color="bg-ice"
        />
        <div class="absolute right-0 top-0 -mt-4">
          <DeltaIndicator :delta="game.deltas?.willpower_delta ?? 0" :decimals="1" />
        </div>
      </div>
    </div>
  </div>
</template>
