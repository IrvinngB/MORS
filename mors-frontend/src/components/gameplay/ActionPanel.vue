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
  <div class="flex flex-col gap-4">
    <h2 class="text-xs uppercase tracking-[0.2em] text-ice/60 font-medium">Acciones</h2>
    
    <div class="flex flex-col gap-2">
      <button
        v-for="action in actions"
        :key="action.id"
        class="group relative px-4 py-3 rounded-lg border transition-all duration-200 text-left overflow-hidden"
        :class="[
          game.isLoading
            ? 'opacity-40 cursor-not-allowed border-white/5 bg-white/[0.02]'
            : action.costly
              ? 'border-warning/30 bg-warning/[0.03] hover:border-warning/50 hover:bg-warning/[0.06]'
              : 'border-white/10 bg-white/[0.02] hover:border-white/20 hover:bg-white/[0.05]',
        ]"
        :disabled="game.isLoading"
        @click="executeAction(action.id)"
      >
        <!-- Hover glow effect -->
        <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700" />
        
        <p class="text-sm font-medium text-snow relative z-10">{{ buttonLabel(action) }}</p>
        <p class="text-xs text-ice/40 mt-0.5 relative z-10">{{ action.description }}</p>
      </button>
    </div>
  </div>
</template>
