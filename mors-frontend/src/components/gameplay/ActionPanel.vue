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
  labelDoubt: string
  labelDespair: string
  description: string
  costly?: boolean
}

const actions = computed<ActionDef[]>(() => [
  {
    id: 'ADVANCE_NORMAL',
    label: 'Avanzar',
    labelDoubt: 'Intentar avanzar...',
    labelDespair: '¿Para qué avanzar?',
    description: 'Sube ~150m',
    costly: false,
  },
  {
    id: 'ADVANCE_AGGRESSIVE',
    label: 'Avanzar Agresivo',
    labelDoubt: 'Forzar el paso...',
    labelDespair: 'Lanzarse al vacío',
    description: 'Sube ~280m, riesgo de caída',
    costly: true,
  },
  {
    id: 'SECURE_ROUTE',
    label: 'Asegurar Ruta',
    labelDoubt: 'Asegurar la salida...',
    labelDespair: '¿Tiene sentido?',
    description: 'Consume cuerda, protege próximos turnos',
    costly: true,
  },
  {
    id: 'CAMP',
    label: 'Acampar',
    labelDoubt: 'Descansar un momento',
    labelDespair: 'Rendirse al frío',
    description: 'Recupera stamina y temperatura',
    costly: true,
  },
  {
    id: 'USE_OXYGEN',
    label: 'Usar Oxígeno',
    labelDoubt: 'Necesito respirar...',
    labelDespair: 'El último canister',
    description: 'Recupera O₂ y voluntad',
    costly: false,
  },
  {
    id: 'EAT',
    label: 'Comer',
    labelDoubt: 'Comer algo...',
    labelDespair: 'La última ración',
    description: 'Recupera stamina',
    costly: false,
  },
  {
    id: 'DESCEND',
    label: 'Descender',
    labelDoubt: 'Quizás bajar...',
    labelDespair: 'Huir de aquí',
    description: 'Baja ~200m',
    costly: false,
  },
  {
    id: 'REST',
    label: 'Descansar',
    labelDoubt: 'Solo un momento...',
    labelDespair: 'No puedo más',
    description: 'Recupera stamina en ruta',
    costly: false,
  },
])

const willpowerState = computed(() => game.willpowerState)

function getLabel(action: ActionDef): string {
  if (willpowerState.value === 'DESPAIR') return action.labelDespair
  if (willpowerState.value === 'DOUBT') return action.labelDoubt
  return action.label
}
</script>

<template>
  <div class="flex flex-col gap-4">
    <h2
      class="text-xs uppercase tracking-[0.2em] font-medium transition-colors duration-500"
      :class="
        willpowerState === 'DESPAIR' ? 'text-danger/60' :
        willpowerState === 'DOUBT'   ? 'text-ice/40' :
                                       'text-ice/60'
      "
    >
      Acciones
    </h2>

    <div class="flex flex-col gap-2">
      <button
        v-for="action in actions"
        :key="action.id"
        id="action-{{ action.id }}"
        class="group relative px-4 py-3 rounded-lg border transition-all duration-200 text-left overflow-hidden"
        :class="[
          game.isLoading
            ? 'opacity-40 cursor-not-allowed border-white/5 bg-white/[0.02]'
            : action.costly
              ? 'border-warning/30 bg-warning/[0.03] hover:border-warning/50 hover:bg-warning/[0.06]'
              : 'border-white/10 bg-white/[0.02] hover:border-white/20 hover:bg-white/[0.05]',
          willpowerState === 'DESPAIR' ? 'despair-button' : '',
        ]"
        :disabled="game.isLoading"
        @click="executeAction(action.id)"
      >
        <!-- Hover glow effect -->
        <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700" />

        <p
          class="text-sm font-medium relative z-10 transition-all duration-500"
          :class="
            willpowerState === 'DESPAIR' ? 'text-danger/70' :
            willpowerState === 'DOUBT'   ? 'text-ice/60' :
                                           'text-snow'
          "
        >
          {{ getLabel(action) }}
        </p>
        <p class="text-xs text-ice/40 mt-0.5 relative z-10">{{ action.description }}</p>
      </button>
    </div>
  </div>
</template>

<style scoped>
/* DESPAIR: buttons tremble slightly */
.despair-button {
  animation: button-tremble 5s ease-in-out infinite;
}

.despair-button:nth-child(odd) {
  animation-delay: 0.3s;
}

.despair-button:nth-child(3n) {
  animation-delay: 0.7s;
}

@keyframes button-tremble {
  0%, 88%, 100% { transform: translateX(0); }
  90%           { transform: translateX(-0.5px) rotate(-0.1deg); }
  92%           { transform: translateX(0.5px) rotate(0.1deg); }
  94%           { transform: translateX(-0.5px); }
  96%           { transform: translateX(0); }
}
</style>
