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
  <div class="relative min-h-screen bg-[#03030a] flex flex-col items-center justify-center overflow-hidden">
    <!-- Deep night gradient & Vignette -->
    <div class="absolute inset-0 bg-gradient-to-b from-[#020205] via-[#08081a] to-peak/20" />
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_30%,rgba(0,0,0,0.8)_100%)] pointer-events-none z-20" />
    
    <!-- Dense Snow particles (decorative) -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none z-10 opacity-60">
      <div v-for="i in 50" :key="i" 
           class="snow-particle"
           :style="{
             left: `${Math.random() * 100}%`,
             animationDelay: `${Math.random() * 10}s`,
             animationDuration: `${5 + Math.random() * 15}s`,
             width: `${Math.random() * 3 + 1}px`,
             height: `${Math.random() * 3 + 1}px`,
             opacity: Math.random() * 0.6 + 0.2
           }"
      />
    </div>

    <!-- Mountain landscape background -->
    <div class="absolute bottom-0 left-0 right-0 pointer-events-none z-0 opacity-40 mix-blend-screen translate-y-12">
      <svg viewBox="0 0 1200 400" class="w-full min-w-[1200px] mx-auto drop-shadow-[0_0_30px_rgba(255,255,255,0.15)]" fill="currentColor">
        <!-- Distant range -->
        <path d="M0 400 L150 250 L250 300 L350 200 L450 280 L550 150 L650 250 L750 180 L850 260 L1000 120 L1100 220 L1200 150 V400 Z" class="text-white/5" />
        <!-- Midground peaks -->
        <path d="M0 400 L200 200 L350 280 L500 100 L650 220 L800 120 L950 250 L1200 80 V400 Z" class="text-white/10" />
        <!-- Main K2 Peak -->
        <path d="M200 400 L450 120 L580 20 L660 110 L760 40 L880 220 L1100 400 Z" class="text-white/20" />
        <!-- Snow caps on main peak -->
        <path d="M580 20 L660 110 L760 40 L700 140 L620 100 L530 150 Z" class="text-white/40" />
      </svg>
    </div>

    <!-- Main Content -->
    <div class="relative z-30 text-center px-6 animate-fade-in w-full max-w-md">
      
      <!-- Title Block -->
      <div class="mb-12 title-breath">
        <h1 class="text-8xl md:text-9xl font-black tracking-[0.25em] text-snow mb-2 drop-shadow-[0_0_20px_rgba(255,255,255,0.4)]" style="margin-right: -0.25em;">
          MORS
        </h1>
        <p class="text-sm md:text-base text-ice/60 italic tracking-[0.2em] font-light">
          Non Omnis Moriar — No todo de mí morirá
        </p>
      </div>

      <!-- Menu Container -->
      <div class="glass-strong rounded-2xl p-8 shadow-2xl border border-white/10 flex flex-col gap-4 backdrop-blur-xl">
        <button
          class="btn-primary w-full text-lg tracking-widest uppercase font-semibold py-4"
          @click="onContinue"
        >
          Continuar
        </button>
        <button
          class="btn-secondary w-full text-lg tracking-widest uppercase font-semibold py-4 border-white/5 hover:border-white/20"
          @click="onStart"
        >
          Nueva Expedición
        </button>
      </div>

      <!-- Footer Description -->
      <p class="mt-12 text-ice/30 text-xs uppercase tracking-widest max-w-sm mx-auto leading-loose">
        Roguelike de supervivencia<br/>
        K2 • 8611m<br/>
        Sin segundas oportunidades
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Slow breathing animation for the title block */
.title-breath {
  animation: breath 8s ease-in-out infinite;
}

@keyframes breath {
  0%, 100% { transform: scale(1); filter: drop-shadow(0 0 20px rgba(255,255,255,0.1)); }
  50% { transform: scale(1.02); filter: drop-shadow(0 0 40px rgba(255,255,255,0.25)); }
}
</style>
