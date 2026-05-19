<script setup lang="ts">
import { useUiStore } from '@/stores/uiStore'

const ui = useUiStore()
</script>

<template>
  <Teleport to="body">
    <div
      v-if="ui.showConfirmModal"
      class="fixed inset-0 bg-black/60 flex items-center justify-center z-50"
      @click.self="ui.closeConfirm"
    >
      <div class="bg-peak rounded-lg p-6 max-w-sm w-full mx-4 border border-snow/20">
        <h3 class="text-lg font-bold text-snow mb-4">Confirmar Acción</h3>
        <p class="text-ice mb-6">{{ ui.confirmMessage }}</p>
        <div class="flex gap-3 justify-end">
          <button
            class="px-4 py-2 rounded border border-snow/30 text-snow hover:bg-snow/10 transition"
            @click="ui.closeConfirm"
          >
            Cancelar
          </button>
          <button
            class="px-4 py-2 rounded bg-warning text-peak font-bold hover:opacity-80 transition"
            @click="$emit('confirm')"
          >
            Confirmar
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>