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
        <div class="glass-strong rounded-xl p-6 max-w-sm w-full border border-white/10 shadow-2xl">
          <h3 class="text-lg font-semibold text-snow mb-3">Confirmar Acción</h3>
          <p class="text-ice/70 mb-6 leading-relaxed">{{ ui.confirmMessage }}</p>
          <div class="flex gap-3 justify-end">
            <button
              class="btn-secondary text-sm px-4 py-2"
              @click="ui.closeConfirm"
            >
              Cancelar
            </button>
            <button
              class="btn-danger text-sm px-4 py-2"
              @click="$emit('confirm')"
            >
              Confirmar
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
