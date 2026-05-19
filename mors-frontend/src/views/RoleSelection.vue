<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useGameStore } from '@/stores/gameStore'
import { useGameLoop } from '@/composables/useGameLoop'

const router = useRouter()
const game = useGameStore()
const { startFresh } = useGameLoop()

interface RoleCard {
  id: string
  name: string
  difficulty: string
  hp_delta: number
  stamina_delta: number
  willpower_delta: number
  stamina_cost_multiplier: number
  equipment: string[]
  ability: string
  description: string
}

const roles: RoleCard[] = [
  {
    id: 'sherpa',
    name: 'Sherpa',
    difficulty: 'Easy',
    hp_delta: 5,
    stamina_delta: 15,
    willpower_delta: -5,
    stamina_cost_multiplier: 0.85,
    equipment: ['+2 Cuerdas'],
    ability: 'Resistencia a caídas (×0.7 probabilidad)',
    description: 'Guía de montaña experimentado. Más eficiente físicamente, pero con menor fuerza de voluntad.',
  },
  {
    id: 'clasico',
    name: 'Alpinista Clásico',
    difficulty: 'Hard',
    hp_delta: 5,
    stamina_delta: 5,
    willpower_delta: 5,
    stamina_cost_multiplier: 1.10,
    equipment: [],
    ability: 'Ninguna — desafío puro',
    description: 'El purista. Buenos stats en todo, pero sin red de seguridad ni habilidad especial.',
  },
  {
    id: 'investigador',
    name: 'Investigador',
    difficulty: 'Medium',
    hp_delta: -10,
    stamina_delta: -15,
    willpower_delta: 20,
    stamina_cost_multiplier: 1.05,
    equipment: ['+10% Oxígeno'],
    ability: 'Bonus de pronóstico (+0.25 confiabilidad)',
    description: 'Científico de altura. Entiende el clima, pero tu cuerpo no está tan preparado.',
  },
  {
    id: 'tecnico',
    name: 'Escalador Técnico',
    difficulty: 'Normal',
    hp_delta: 0,
    stamina_delta: 0,
    willpower_delta: 0,
    stamina_cost_multiplier: 0.95,
    equipment: ['+2 Cuerdas', '+1 Gas'],
    ability: 'Descuento de altitud (≥7000m, ×0.90 stamina)',
    description: 'Especialista en terreno vertical. Equipado para lo técnico, más eficiente en altura.',
  },
  {
    id: 'medico',
    name: 'Médico de Expedición',
    difficulty: 'Medium',
    hp_delta: -5,
    stamina_delta: -10,
    willpower_delta: 15,
    stamina_cost_multiplier: 1.0,
    equipment: ['+2 Raciones', '+10% Oxígeno'],
    ability: 'Curación gratuita (+15HP una vez) + mitigación de daño (×0.80)',
    description: 'Doctor de montaña. Sabe mantenerse vivo cuando el cuerpo falla.',
  },
]

const difficultyColor: Record<string, string> = {
  Easy: 'bg-success/20 text-success border-success/30',
  Normal: 'bg-warning/20 text-warning border-warning/30',
  Medium: 'bg-warning/20 text-warning border-warning/30',
  Hard: 'bg-danger/20 text-danger border-danger/30',
}

async function onSelectRole(roleId: string) {
  await startFresh(roleId)
  if (game.sessionId) router.push('/game')
}

function onBack() {
  router.push('/')
}

function formatDelta(value: number): string {
  return value > 0 ? `+${value}` : `${value}`
}
</script>

<template>
  <div class="relative min-h-screen bg-[#03030a] flex flex-col items-center justify-center overflow-hidden px-4 py-8">
    <!-- Background gradient -->
    <div class="absolute inset-0 bg-gradient-to-b from-[#020205] via-[#08081a] to-peak/20" />
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_30%,rgba(0,0,0,0.8)_100%)] pointer-events-none z-20" />

    <!-- Content -->
    <div class="relative z-30 w-full max-w-5xl animate-fade-in">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-4xl md:text-5xl font-black tracking-[0.15em] text-snow mb-2">
          Elige tu Rol
        </h1>
        <p class="text-ice/50 text-sm tracking-wider">
          Cada rol modifica tus stats iniciales, equipo y habilidades especiales
        </p>
      </div>

      <!-- Role Cards Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4 mb-8">
        <div
          v-for="role in roles"
          :key="role.id"
          class="glass-strong rounded-xl p-5 border border-white/10 flex flex-col gap-3 backdrop-blur-xl hover:border-white/20 transition-colors duration-200"
        >
          <!-- Name + Difficulty -->
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-bold text-snow tracking-wide">{{ role.name }}</h2>
            <span
              class="text-xs px-2 py-0.5 rounded-full border font-medium"
              :class="difficultyColor[role.difficulty]"
            >
              {{ role.difficulty }}
            </span>
          </div>

          <!-- Description -->
          <p class="text-ice/60 text-xs leading-relaxed">{{ role.description }}</p>

          <!-- Stat Deltas -->
          <div class="grid grid-cols-3 gap-2 text-center">
            <div class="bg-white/5 rounded-lg py-2">
              <div class="text-xs text-ice/40 uppercase tracking-wider">HP</div>
              <div
                class="text-sm font-bold"
                :class="role.hp_delta >= 0 ? 'text-success' : 'text-danger'"
              >
                {{ formatDelta(role.hp_delta) }}
              </div>
            </div>
            <div class="bg-white/5 rounded-lg py-2">
              <div class="text-xs text-ice/40 uppercase tracking-wider">Stamina</div>
              <div
                class="text-sm font-bold"
                :class="role.stamina_delta >= 0 ? 'text-success' : 'text-danger'"
              >
                {{ formatDelta(role.stamina_delta) }}
              </div>
            </div>
            <div class="bg-white/5 rounded-lg py-2">
              <div class="text-xs text-ice/40 uppercase tracking-wider">Will</div>
              <div
                class="text-sm font-bold"
                :class="role.willpower_delta >= 0 ? 'text-success' : 'text-danger'"
              >
                {{ formatDelta(role.willpower_delta) }}
              </div>
            </div>
          </div>

          <!-- Stamina Cost -->
          <div v-if="role.stamina_cost_multiplier !== 1.0" class="text-xs text-ice/50">
            Costo stamina:
            <span
              :class="role.stamina_cost_multiplier < 1.0 ? 'text-success' : 'text-danger'"
            >
              ×{{ role.stamina_cost_multiplier.toFixed(2) }}
            </span>
          </div>

          <!-- Equipment -->
          <div v-if="role.equipment.length > 0" class="flex flex-wrap gap-1">
            <span
              v-for="item in role.equipment"
              :key="item"
              class="text-xs bg-ice/10 text-ice/70 px-2 py-0.5 rounded"
            >
              {{ item }}
            </span>
          </div>

          <!-- Ability -->
          <div class="text-xs text-mors/80 border-t border-white/5 pt-2 mt-1">
            <span class="text-ice/40 uppercase tracking-wider text-[10px]">Habilidad:</span>
            <span class="block mt-0.5">{{ role.ability }}</span>
          </div>

          <!-- Select Button -->
          <button
            class="btn-primary w-full text-sm tracking-widest uppercase font-semibold py-3 mt-2"
            @click="onSelectRole(role.id)"
          >
            Seleccionar
          </button>
        </div>
      </div>

      <!-- Back Button -->
      <div class="text-center">
        <button
          class="text-ice/50 hover:text-snow transition-colors duration-200 text-sm tracking-wider"
          @click="onBack"
        >
          ← Volver al Menú
        </button>
      </div>
    </div>
  </div>
</template>
