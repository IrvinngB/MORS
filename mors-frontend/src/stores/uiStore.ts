import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
  const showConfirmModal = ref(false)
  const confirmAction = ref<string | null>(null)
  const confirmMessage = ref<string>('')
  const showEventBanner = ref(false)
  const eventBannerText = ref<string>('')

  function openConfirm(action: string, message: string) {
    confirmAction.value = action
    confirmMessage.value = message
    showConfirmModal.value = true
  }

  function closeConfirm() {
    showConfirmModal.value = false
    confirmAction.value = null
    confirmMessage.value = ''
  }

  function triggerEventBanner(text: string) {
    eventBannerText.value = text
    showEventBanner.value = true
    setTimeout(() => { showEventBanner.value = false }, 3000)
  }

  return {
    showConfirmModal,
    confirmAction,
    confirmMessage,
    showEventBanner,
    eventBannerText,
    openConfirm,
    closeConfirm,
    triggerEventBanner,
  }
})