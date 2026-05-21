import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
  const showConfirmModal = ref(false)
  const confirmAction = ref<string | null>(null)
  const confirmMessage = ref<string>('')
  const confirmIsDanger = ref(false)
  const showEventBanner = ref(false)
  const eventBannerText = ref<string>('')
  const eventBannerType = ref<string>('warning')
  const actionError = ref<string | null>(null)

  function openConfirm(action: string, message: string, isDanger = false) {
    confirmAction.value = action
    confirmMessage.value = message
    confirmIsDanger.value = isDanger
    showConfirmModal.value = true
  }

  function closeConfirm() {
    showConfirmModal.value = false
    confirmAction.value = null
    confirmMessage.value = ''
    confirmIsDanger.value = false
  }

  function triggerEventBanner(text: string, eventType?: string) {
    eventBannerText.value = text
    eventBannerType.value = _resolveEventSeverity(eventType ?? '')
    showEventBanner.value = true
    const duration = _resolveBannerDuration(eventType ?? '')
    setTimeout(() => { showEventBanner.value = false }, duration)
  }

  function showActionError(message: string) {
    actionError.value = message
    setTimeout(() => { actionError.value = null }, 4000)
  }

  function showWarningBanner(text: string, duration = 6000) {
    eventBannerText.value = text
    eventBannerType.value = 'warning'
    showEventBanner.value = true
    setTimeout(() => { showEventBanner.value = false }, duration)
  }

  function clearActionError() {
    actionError.value = null
  }

  return {
    showConfirmModal,
    confirmAction,
    confirmMessage,
    confirmIsDanger,
    showEventBanner,
    eventBannerText,
    eventBannerType,
    actionError,
    openConfirm,
    closeConfirm,
    triggerEventBanner,
    showActionError,
    clearActionError,
    showWarningBanner,
  }
})

function _resolveEventSeverity(eventType: string): string {
  const dangerEvents = ['PULMONARY_EDEMA', 'DEAD_FALL', 'FROSTBITE']
  const successEvents = ['SECOND_WIND']
  const infoEvents = ['PARTNER_VISION', 'DISTANT_AVALANCHE']
  if (dangerEvents.includes(eventType)) return 'danger'
  if (successEvents.includes(eventType)) return 'success'
  if (infoEvents.includes(eventType)) return 'info'
  return 'warning'
}

function _resolveBannerDuration(eventType: string): number {
  const criticalEvents = ['PULMONARY_EDEMA', 'O2_REGULATOR_FAIL', 'TENT_COLLAPSE']
  if (criticalEvents.includes(eventType)) return 5000
  return 3500
}