<script setup lang="ts">
import { computed } from 'vue'
import { useGameStore } from '@/stores/gameStore'
import { useGameLoop } from '@/composables/useGameLoop'
import type { ActionType } from '@/api/types'

const game = useGameStore()
const { executeAction } = useGameLoop()

interface ActionDef {
  id: ActionType
  label: string
  description: string
  costly?: boolean
}

const actions = computed<ActionDef[]>(() => [
  { id: 'ADVANCE_NORMAL', label: 'Avanzar', description: 'Sube ~150m', costly: false },
  { id: 'ADVANCE_AGGRESSIVE', label: 'Avanzar Agresivo', description: 'Sube ~280m, riesgo de caída', costly: true },
  { id: 'SECURE_ROUTE', label: 'Asegurar Ruta', description: 'Consume cuerda, protege próximos turnos', costly: true },
  { id: 'CAMP', label: 'Acampar', description: 'Recupera stamina y temperatura', costly: true },
  { id: 'USE_OXYGEN', label: 'Usar Oxígeno', description: 'Recupera O₂ y voluntad', costly: false },
  { id: 'EAT', label: 'Comer', description: 'Recupera stamina levemente', costly: false },
  { id: 'DESCEND', label: 'Descender', description: 'Baja ~200m', costly: false },
  { id: 'REST', label: 'Descansar', description: 'Recupera stamina en ruta', costly: false },
])

const willpower = computed(() => game.state?.player?.willpower ?? 100)

function buttonLabel(action: ActionDef) {
  if (willpower.value < 30) return '¿Seguir...?'
  return action.label
}
</script>

<template>
  <div class="flex flex-col gap-3">
    <h2 class="text-xs uppercase tracking-widest text-ice mb-1">Acciones</h2>
    <div class="flex flex-col gap-2">
      <button
        v-for="action in actions"
        :key="action.id"
        class="px-3 py-2 rounded border transition text-left"
        :class="[
          game.isLoading
            ? 'opacity-50 cursor-not-allowed border-ice/30 text-ice'
            : 'border-glacier/50 text-snow hover:bg-glacier/20',
        ]"
        :disabled="game.isLoading"
        @click="executeAction(action.id)"
      >
        <p class="text-sm font-medium">{{ buttonLabel(action) }}</p>
        <p class="text-xs text-ice">{{ action.description }}</p>
      </button>
    </div>
  </div>
</template>