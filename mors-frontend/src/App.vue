<script setup lang="ts">
import { RouterView, useRouter } from 'vue-router'
import { watch } from 'vue'
import { useGameStore } from '@/stores/gameStore'

const game = useGameStore()
const router = useRouter()

watch(
  () => game.status,
  (status) => {
    if (status === 'SUMMIT') router.push('/summit')
    if (status === 'DEAD') router.push('/gameover')
  }
)
</script>

<template>
  <RouterView />
</template>