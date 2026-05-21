<script setup lang="ts">
import { useUiStore } from '@/stores/uiStore'

const ui = useUiStore()
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="ui.showConfirmModal"
        class="fixed inset-0 bg-abyss/80 backdrop-blur-sm flex items-center justify-center z-50 p-4"
        @click.self="ui.closeConfirm"
      >
        <div
          class="glass-strong rounded-xl p-6 max-w-sm w-full shadow-2xl"
          :class="ui.confirmIsDanger ? 'border-2 border-danger/60 shadow-[0_0_30px_rgba(231,76,60,0.2)]' : 'border border-white/10'"
        >
          <!-- Danger icon -->
          <div v-if="ui.confirmIsDanger" class="flex items-center gap-2 mb-3">
            <svg class="w-6 h-6 text-danger shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
              <line x1="12" y1="9" x2="12" y2="13" />
              <line x1="12" y1="17" x2="12.01" y2="17" />
            </svg>
            <h3 class="text-lg font-semibold text-danger">Acción Peligrosa</h3>
          </div>
          <h3 v-else class="text-lg font-semibold text-snow mb-3">Confirmar Acción</h3>

          <p
            class="mb-6 leading-relaxed"
            :class="ui.confirmIsDanger ? 'text-danger/90 text-sm font-medium' : 'text-ice/70'"
          >
            {{ ui.confirmMessage }}
          </p>

          <div class="flex gap-3 justify-end">
            <button
              class="btn-secondary text-sm px-4 py-2"
              @click="ui.closeConfirm"
            >
              Cancelar
            </button>
            <button
              class="text-sm px-4 py-2 font-semibold rounded-lg border transition-all duration-200"
              :class="ui.confirmIsDanger
                ? 'border-danger/50 bg-danger/15 text-danger hover:bg-danger/25 hover:border-danger/70'
                : 'border-danger/30 bg-danger/8 text-danger hover:bg-danger/15'"
              @click="$emit('confirm')"
            >
              {{ ui.confirmIsDanger ? 'Confirmar' : 'Confirmar' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
