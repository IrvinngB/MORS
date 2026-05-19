<script setup lang="ts">
import { useGameStore } from '@/stores/gameStore'
import { useGameLoop } from '@/composables/useGameLoop'
import { useRouter } from 'vue-router'

const game = useGameStore()
const { startFresh, startOrResume } = useGameLoop()
const router = useRouter()

async function onStart() {
  await startFresh()
  if (game.sessionId) router.push('/game')
}

async function onContinue() {
  await startOrResume()
  if (game.sessionId) router.push('/game')
}
</script>

<template>
  <div class="relative min-h-screen bg-mors flex flex-col items-center justify-center overflow-hidden">
    <!-- Background gradient -->
    <div class="absolute inset-0 bg-gradient-to-b from-abyss via-mors to-peak/30" />
    
    <!-- Snow particles (decorative) -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div v-for="i in 30" :key="i" 
           class="snow-particle"
           :style="{
             left: `${Math.random() * 100}%`,
             animationDelay: `${Math.random() * 10}s`,
             animationDuration: `${8 + Math.random() * 12}s`,
             opacity: Math.random() * 0.5 + 0.1
           }"
      />
    </div>

    <!-- Content -->
    <div class="relative z-10 text-center px-6 animate-fade-in">
      <!-- Title -->
      <h1 class="text-8xl md:text-9xl font-black tracking-[0.3em] text-snow mb-4 drop-shadow-2xl">
        MORS
      </h1>
      
      <!-- Subtitle -->
      <p class="text-lg md:text-xl text-ice/70 italic tracking-widest mb-16 font-light">
        Non Omnis Moriar — No Todo de Mí Morirá
      </p>

      <!-- Mountain silhouette decoration -->
      <div class="mb-16 opacity-20">
        <svg viewBox="0 0 800 200" class="w-96 h-24 mx-auto" fill="currentColor" color="currentColor">
          <path d="M0 200 L200 80 L350 140 L500 20 L650 100 L800 200 Z" />
        </svg>
      </div>

      <!-- Buttons -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
        <button
          class="btn-primary min-w-[200px] text-lg tracking-wide"
          @click="onContinue"
        >
          Continuar Partida
        </button>
        <button
          class="btn-secondary min-w-[200px] text-lg tracking-wide"
          @click="onStart"
        >
          Nueva Partida
        </button>
      </div>

      <!-- Description -->
      <p class="mt-16 text-ice/40 text-sm max-w-md mx-auto leading-relaxed">
        Roguelike de supervivencia en alta montaña. 
        Cada turno representa una hora de expedición. 
        No hay guardado automático. No hay segunda oportunidad.
      </p>
    </div>

    <!-- Bottom gradient fade -->
    <div class="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-mors to-transparent pointer-events-none" />
  </div>
</template>
