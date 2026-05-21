<script setup lang="ts">
import { computed } from 'vue'
import { useGameStore } from '@/stores/gameStore'
import { useUiStore } from '@/stores/uiStore'
import { useGameLoop } from '@/composables/useGameLoop'
import type { ActionType } from '@/api/types'

const game = useGameStore()
const ui = useUiStore()
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
    description: 'Sube aproximadamente 150m',
    costly: false,
  },
  {
    id: 'ADVANCE_AGGRESSIVE',
    label: 'Avanzar Agresivo',
    labelDoubt: 'Forzar el paso...',
    labelDespair: 'Lanzarse al vacío',
    description: 'Sube aproximadamente 280m, riesgo de caída',
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
    labelDespair: 'El último tanque',
    description: 'Consume 1 tanque O₂, recupera O₂ y voluntad',
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
    description: 'Baja aproximadamente 200m',
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
  ...(game.state?.role === 'medico' && !game.state?.free_heal_used ? [{
    id: 'USE_FREE_HEAL' as ActionType,
    label: 'Curación de Emergencia',
    labelDoubt: 'Usar los suministros médicos...',
    labelDespair: 'La última jeringa',
    description: 'Recupera +15 HP (uso único)',
    costly: false,
  }] : []),
])

const movementActionIds = ['ADVANCE_NORMAL', 'ADVANCE_AGGRESSIVE', 'DESCEND']

const movementActions = computed(() => {
  return actions.value.filter(a => movementActionIds.includes(a.id))
})

const survivalActions = computed(() => {
  return actions.value.filter(a => !movementActionIds.includes(a.id))
})

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
  let wpMod = 1.0
  if (wp < 10) wpMod = 1.25
  else if (wp < 20) wpMod = 1.15
  else if (wp < 30) wpMod = 1.05

  let roleMult = 1.0
  const role = game.state.role
  if (role === 'sherpa') {
    roleMult = 0.85
  } else if (role === 'clasico') {
    roleMult = 1.1
  } else if (role === 'tecnico') {
    if (alt >= 7000) roleMult = 0.95 * 0.90
    else roleMult = 0.95
  } else if (role === 'investigador') {
    roleMult = 1.0
  } else if (role === 'medico') {
    roleMult = 1.0
  }

  const totalMod = altFactor * weatherMod * oxMod * wpMod * roleMult
  const baseCost = 12.0 * totalMod

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
  breakdown += `• Base: 12\n`
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

function isActionDisabled(actionId: ActionType): boolean {
  if (game.isLoading) return true

  switch (actionId) {
    case 'EAT':
      return !game.canEat
    case 'USE_OXYGEN':
      return !game.canUseOxygen
    case 'SECURE_ROUTE':
      return !game.canSecureRoute
    case 'USE_FREE_HEAL':
      return !game.canFreeHeal
    case 'ADVANCE_NORMAL':
    case 'ADVANCE_AGGRESSIVE':
      return !game.canAdvance
    default:
      return false
  }
}

function getDisabledReason(actionId: ActionType): string {
  switch (actionId) {
    case 'EAT':
      return 'Sin raciones de comida disponibles'
    case 'USE_OXYGEN':
      return 'Sin tanques de oxígeno disponibles'
    case 'SECURE_ROUTE':
      return 'Sin cuerdas disponibles'
    case 'USE_FREE_HEAL':
      return game.state?.role !== 'medico'
        ? 'Solo disponible para el Médico de Expedición'
        : 'Curación gratuita ya utilizada'
    case 'ADVANCE_NORMAL':
    case 'ADVANCE_AGGRESSIVE':
      return 'Visibilidad cero por ventisca — se necesita cuerda para avanzar'
    default:
      return ''
  }
}
</script>

<template>
  <div class="flex flex-col gap-4">
    <!-- Validation Error Banner -->
    <Transition name="error-fade">
      <div
        v-if="ui.actionError"
        class="px-3 py-2 rounded-lg border border-danger/40 bg-danger/10 text-xs text-danger flex items-center gap-2"
      >
        <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <span>{{ ui.actionError }}</span>
        <button
          class="ml-auto text-danger/50 hover:text-danger transition-colors"
          @click="ui.clearActionError()"
        >
          <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>
    </Transition>

    <!-- Block: Movement Actions -->
    <div class="flex flex-col gap-2">
      <h3 
        class="text-[10px] uppercase tracking-[0.2em] font-bold mb-1 select-none"
        :class="willpowerState === 'DESPAIR' ? 'text-danger/50' : 'text-glacier/60'"
      >
        Movimiento de Ascenso
      </h3>
      <div class="flex flex-col gap-1.5">
        <button
          v-for="action in movementActions"
          :key="action.id"
          :id="'action-' + action.id"
          class="group relative px-3 py-2.5 rounded-lg border transition-all duration-200 text-left overflow-hidden"
          :class="[
            isActionDisabled(action.id)
              ? 'opacity-30 cursor-not-allowed border-white/5 bg-white/[0.02]'
              : game.isLoading
                ? 'opacity-40 cursor-not-allowed border-white/5 bg-white/[0.02]'
                : action.costly
                  ? 'border-warning/30 bg-warning/[0.03] hover:border-warning/50 hover:bg-warning/[0.06] cursor-pointer'
                  : 'border-glacier/15 bg-glacier/[0.02] hover:border-glacier/30 hover:bg-glacier/[0.05] cursor-pointer',
            willpowerState === 'DESPAIR' ? 'despair-button' : '',
          ]"
          :disabled="isActionDisabled(action.id)"
          :title="isActionDisabled(action.id) ? getDisabledReason(action.id) : getActionTooltip(action.id)"
          @click="executeAction(action.id)"
        >
          <!-- Shiny hover effect (only when not disabled) -->
          <div v-if="!isActionDisabled(action.id)" class="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700 pointer-events-none" />

          <div class="flex justify-between items-center relative z-10">
            <div>
              <p
                class="text-xs font-semibold tracking-wide transition-all duration-500"
                :class="
                  isActionDisabled(action.id) ? 'text-ice/30' :
                  willpowerState === 'DESPAIR' ? 'text-danger/80' :
                  willpowerState === 'DOUBT'   ? 'text-ice/70' :
                                                 'text-snow'
                "
              >
                {{ getLabel(action) }}
              </p>
              <p class="text-[10px] mt-0.5 leading-tight"
                :class="isActionDisabled(action.id) ? 'text-ice/20' : 'text-ice/45'"
              >{{ action.description }}</p>
            </div>
          </div>
        </button>
      </div>
    </div>

    <!-- Block: Survival / Resource Actions -->
    <div class="flex flex-col gap-2">
      <h3 
        class="text-[10px] uppercase tracking-[0.2em] font-bold mb-1 select-none"
        :class="willpowerState === 'DESPAIR' ? 'text-danger/50' : 'text-ice/50'"
      >
        Supervivencia y Soporte
      </h3>
      <div class="flex flex-col gap-1.5">
        <button
          v-for="action in survivalActions"
          :key="action.id"
          :id="'action-' + action.id"
          class="group relative px-3 py-2.5 rounded-lg border transition-all duration-200 text-left overflow-hidden"
          :class="[
            isActionDisabled(action.id)
              ? 'opacity-30 cursor-not-allowed border-white/5 bg-white/[0.02]'
              : game.isLoading
                ? 'opacity-40 cursor-not-allowed border-white/5 bg-white/[0.02]'
                : action.costly
                  ? 'border-warning/30 bg-warning/[0.03] hover:border-warning/50 hover:bg-warning/[0.06] cursor-pointer'
                  : 'border-white/10 bg-white/[0.02] hover:border-white/25 hover:bg-white/[0.06] cursor-pointer',
            willpowerState === 'DESPAIR' ? 'despair-button' : '',
          ]"
          :disabled="isActionDisabled(action.id)"
          :title="isActionDisabled(action.id) ? getDisabledReason(action.id) : ''"
          @click="executeAction(action.id)"
        >
          <!-- Shiny hover effect (only when not disabled) -->
          <div v-if="!isActionDisabled(action.id)" class="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700 pointer-events-none" />

          <div class="flex justify-between items-center relative z-10">
            <div>
              <p
                class="text-xs font-semibold tracking-wide transition-all duration-500"
                :class="
                  isActionDisabled(action.id) ? 'text-ice/30' :
                  willpowerState === 'DESPAIR' ? 'text-danger/80' :
                  willpowerState === 'DOUBT'   ? 'text-ice/70' :
                                                 'text-snow'
                "
              >
                {{ getLabel(action) }}
              </p>
              <p class="text-[10px] mt-0.5 leading-tight"
                :class="isActionDisabled(action.id) ? 'text-ice/20' : 'text-ice/45'"
              >{{ action.description }}</p>
            </div>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Error banner transition */
.error-fade-enter-active { transition: all 0.3s ease-out; }
.error-fade-leave-active { transition: all 0.3s ease-in; }
.error-fade-enter-from,
.error-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

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
