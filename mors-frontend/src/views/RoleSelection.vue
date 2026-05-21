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
    equipment: ['5 Cuerdas', '3 Tanques O₂', '10 Raciones', '5 Gas'],
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
    equipment: ['1 Cuerda', '0 Tanques O₂', '8 Raciones', '3 Gas'],
    ability: 'Ninguna — desafío puro',
    description: 'El purista. Buenos stats en todo, pero sin red de seguridad ni habilidad especial.',
  },
  {
    id: 'investigador',
    name: 'Investigador',
    difficulty: 'Medium',
    hp_delta: -5,
    stamina_delta: -5,
    willpower_delta: 15,
    stamina_cost_multiplier: 1.0,
    equipment: ['3 Cuerdas', '4 Tanques O₂', '10 Raciones', '5 Gas'],
    ability: 'Bonus de pronóstico (+0.25 confiabilidad)',
    description: 'Científico de altura. Entiende el clima mejor que nadie. Leve penalización física.',
  },
  {
    id: 'tecnico',
    name: 'Escalador Técnico',
    difficulty: 'Normal',
    hp_delta: 0,
    stamina_delta: 0,
    willpower_delta: 0,
    stamina_cost_multiplier: 0.95,
    equipment: ['5 Cuerdas', '3 Tanques O₂', '10 Raciones', '6 Gas'],
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
    equipment: ['3 Cuerdas', '4 Tanques O₂', '12 Raciones', '5 Gas'],
    ability: 'Curación gratuita (+15HP una vez) + mitigación de daño (×0.80)',
    description: 'Doctor de montaña. Sabe mantenerse vivo cuando el cuerpo falla.',
  },
]

const difficultyColor: Record<string, string> = {
  Easy: 'bg-success/20 text-success border-success/30',
  Normal: 'bg-mors/20 text-mors border-mors/30',
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

function formatCostMult(mult: number): string {
  if (mult < 1.0) return `−${((1 - mult) * 100).toFixed(0)}%`
  if (mult > 1.0) return `+${((mult - 1) * 100).toFixed(0)}%`
  return 'normal'
}
</script>

<template>
  <div class="relative min-h-screen bg-[#03030a] flex flex-col items-center overflow-hidden px-4 py-8">
    <!-- Background gradient -->
    <div class="absolute inset-0 bg-gradient-to-b from-[#020205] via-[#08081a] to-peak/20" />
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_30%,rgba(0,0,0,0.8)_100%)] pointer-events-none z-20" />

    <!-- Content -->
    <div class="relative z-30 w-full max-w-6xl animate-fade-in">
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
          class="glass-strong rounded-xl p-4 border border-white/10 flex flex-col gap-2.5 backdrop-blur-xl hover:border-white/20 transition-colors duration-200"
        >
          <!-- Name + Difficulty -->
          <div class="flex items-center justify-between">
            <h2 class="text-base font-bold text-snow tracking-wide">{{ role.name }}</h2>
            <span
              class="text-[10px] px-1.5 py-0.5 rounded-full border font-semibold uppercase tracking-wider"
              :class="difficultyColor[role.difficulty]"
            >
              {{ role.difficulty }}
            </span>
          </div>

          <!-- Description -->
          <p class="text-ice/60 text-[11px] leading-relaxed">{{ role.description }}</p>

          <!-- Stat Deltas - clean list layout -->
          <div class="flex flex-col gap-1.5">
            <div class="flex items-center justify-between text-xs">
              <span class="text-ice/40 uppercase tracking-wider text-[10px]">HP</span>
              <span
                class="font-bold text-sm"
                :class="role.hp_delta >= 0 ? 'text-success' : 'text-danger'"
              >
                {{ formatDelta(role.hp_delta) }}
              </span>
            </div>
            <div class="flex items-center justify-between text-xs">
              <span class="text-ice/40 uppercase tracking-wider text-[10px]">Stamina</span>
              <span
                class="font-bold text-sm"
                :class="role.stamina_delta >= 0 ? 'text-success' : 'text-danger'"
              >
                {{ formatDelta(role.stamina_delta) }}
              </span>
            </div>
            <div class="flex items-center justify-between text-xs">
              <span class="text-ice/40 uppercase tracking-wider text-[10px]">Willpower</span>
              <span
                class="font-bold text-sm"
                :class="role.willpower_delta >= 0 ? 'text-success' : 'text-danger'"
              >
                {{ formatDelta(role.willpower_delta) }}
              </span>
            </div>
          </div>

          <!-- Stamina Cost -->
          <div class="flex items-center justify-between text-xs">
            <span class="text-ice/40 uppercase tracking-wider text-[10px]">Costo stamina</span>
            <span
              class="font-bold text-sm"
              :class="role.stamina_cost_multiplier < 1.0 ? 'text-success' : role.stamina_cost_multiplier > 1.0 ? 'text-danger' : 'text-ice/50'"
            >
              {{ formatCostMult(role.stamina_cost_multiplier) }}
            </span>
          </div>

          <!-- Equipment -->
          <div v-if="role.equipment.length > 0" class="flex flex-wrap gap-1">
            <span
              v-for="item in role.equipment"
              :key="item"
              class="text-[10px] bg-ice/10 text-ice/70 px-1.5 py-0.5 rounded"
            >
              {{ item }}
            </span>
          </div>

          <!-- Ability -->
          <div class="text-[11px] text-ice/80 border-t border-white/5 pt-2">
            <span class="text-ice/40 uppercase tracking-wider text-[9px]">Habilidad:</span>
            <span class="block mt-0.5 leading-snug">{{ role.ability }}</span>
          </div>

          <!-- Select Button -->
          <button
            class="btn-primary w-full text-xs tracking-widest uppercase font-semibold py-2.5 mt-1"
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
