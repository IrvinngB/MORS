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

const WEATHER_MODIFIERS: Record<string, number> = {
  CLEAR: 1.0,
  CLOUDY: 1.2,
  WIND: 1.5,
  STORM: 2.0,
  WHITEOUT: 3.0,
}

const estimateStaminaCost = computed(() => {
  if (!game.state) return null
  const player = game.state.player
  const consumables = game.state.consumables
  
  const alt = player.altitude
  const altFactor = 1 + Math.pow(alt / 8000, 2)
  const weather = game.state.weather
  const weatherMod = WEATHER_MODIFIERS[weather] ?? 1.0
  
  let oxMod = 1.0
  const o2 = consumables.oxygen_pct
  const valve = consumables.oxygen_valve_open
  if (valve && o2 > 0) {
    oxMod = 0.75
  } else {
    let baseMod = 1.0
    if (o2 > 50) baseMod = 0.8
    else if (o2 < 30) baseMod = 1.4
    
    if (alt >= 7000) {
      oxMod = baseMod * 1.3
    } else {
      oxMod = baseMod
    }
  }
  
  const wp = player.willpower
  const wpMod = wp < 20 ? 1.15 : 1.0
  
  let roleMult = 1.0
  const role = game.state.role
  if (role === 'sherpa') {
    roleMult = 0.9
  } else if (role === 'clasico') {
    roleMult = 1.1
  } else if (role === 'tecnico' && alt >= 7000) {
    roleMult = 0.7
  }
  
  const totalMod = altFactor * weatherMod * oxMod * wpMod * roleMult
  const baseCost = 15.0 * totalMod
  
  return {
    base: baseCost,
    factors: {
      altFactor,
      weatherMod,
      oxMod,
      wpMod,
      roleMult,
    }
  }
})

function getActionCost(actionId: ActionType): number | null {
  if (!estimateStaminaCost.value || !game.state) return null
  const baseCost = estimateStaminaCost.value.base
  const consecutive = game.state.player.consecutive_aggressive_actions ?? 0
  
  if (actionId === 'ADVANCE_NORMAL') {
    return Math.round(baseCost * 1.0)
  }
  if (actionId === 'ADVANCE_AGGRESSIVE') {
    return Math.round(baseCost * 1.5 * (1 + consecutive * 0.1))
  }
  if (actionId === 'SECURE_ROUTE') {
    return Math.round(baseCost * 0.8)
  }
  if (actionId === 'DESCEND') {
    return Math.round(baseCost * 0.3)
  }
  return null
}

function getActionTooltip(actionId: ActionType): string {
  const est = estimateStaminaCost.value
  if (!est || !game.state) return ''
  const cost = getActionCost(actionId)
  if (cost === null) return ''
  
  const consecutive = game.state.player.consecutive_aggressive_actions ?? 0
  
  let breakdown = `Estimación del costo de Stamina: ~${cost}\n`
  breakdown += `• Base: 15\n`
  breakdown += `• Altitud: x${est.factors.altFactor.toFixed(2)}\n`
  if (est.factors.weatherMod !== 1.0) breakdown += `• Clima: x${est.factors.weatherMod.toFixed(1)}\n`
  if (est.factors.oxMod !== 1.0) breakdown += `• Oxígeno: x${est.factors.oxMod.toFixed(2)}\n`
  if (est.factors.wpMod !== 1.0) breakdown += `• Voluntad: x${est.factors.wpMod.toFixed(2)}\n`
  if (est.factors.roleMult !== 1.0) breakdown += `• Rol: x${est.factors.roleMult.toFixed(2)}\n`
  
  if (actionId === 'ADVANCE_AGGRESSIVE') {
    breakdown += `• Esfuerzo Agresivo: x1.5\n`
    if (consecutive > 0) {
      breakdown += `• Fatiga acumulada: +${consecutive * 10}%\n`
    }
  } else if (actionId === 'SECURE_ROUTE') {
    breakdown += `• Asegurar Ruta: x0.8\n`
  } else if (actionId === 'DESCEND') {
    breakdown += `• Descenso: x0.3\n`
  }
  
  return breakdown.trim()
}

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
        :id="'action-' + action.id"
        :title="getActionTooltip(action.id)"
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

        <div class="flex justify-between items-start relative z-10">
          <div>
            <p
              class="text-sm font-medium transition-all duration-500"
              :class="
                willpowerState === 'DESPAIR' ? 'text-danger/70' :
                willpowerState === 'DOUBT'   ? 'text-ice/60' :
                                               'text-snow'
              "
            >
              {{ getLabel(action) }}
            </p>
            <p class="text-xs text-ice/40 mt-0.5">{{ action.description }}</p>
          </div>
          <!-- Stamina cost indicator -->
          <div v-if="getActionCost(action.id) !== null" class="text-right flex items-center">
            <span class="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-white/5 border border-white/5 text-ice/60 group-hover:text-snow transition-colors duration-200">
              ⚡ {{ getActionCost(action.id) }}
            </span>
          </div>
        </div>
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
