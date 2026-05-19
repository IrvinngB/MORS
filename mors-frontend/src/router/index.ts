import { createRouter, createWebHistory } from 'vue-router'
import MainMenu from '@/views/MainMenu.vue'
import GameView from '@/views/GameView.vue'
import SummitView from '@/views/SummitView.vue'
import GameOver from '@/views/GameOver.vue'
import RoleSelection from '@/views/RoleSelection.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: MainMenu },
    { path: '/role-selection', name: 'role-selection', component: RoleSelection },
    { path: '/game', name: 'game', component: GameView },
    { path: '/summit', name: 'summit', component: SummitView },
    { path: '/gameover', name: 'gameover', component: GameOver },
  ],
})

export default router