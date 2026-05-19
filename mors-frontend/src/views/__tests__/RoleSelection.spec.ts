import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import RoleSelection from '@/views/RoleSelection.vue'
import * as gameApi from '@/api/game'

// Mock vue-router
vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}))

// Mock the API
vi.mock('@/api/game', () => ({
  newGame: vi.fn(),
}))

// Mock useGameLoop composable
vi.mock('@/composables/useGameLoop', () => ({
  useGameLoop: () => ({
    startFresh: vi.fn(async (role?: string) => {
      // Simulate what the real composable does
      const gameStore = useGameStore()
      await gameStore.startGame(role)
    }),
    startOrResume: vi.fn(),
    executeAction: vi.fn(),
    confirmAction: vi.fn(),
  }),
}))

import { useGameStore } from '@/stores/gameStore'

const ROLE_NAMES = ['Sherpa', 'Alpinista Clásico', 'Investigador', 'Escalador Técnico', 'Médico de Expedición']
const ROLE_IDS = ['sherpa', 'clasico', 'investigador', 'tecnico', 'medico']
const DIFFICULTIES = ['Easy', 'Hard', 'Medium', 'Normal', 'Medium']

describe('RoleSelection.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('renders the page title', () => {
    const wrapper = mount(RoleSelection, {
      global: {
        stubs: ['router-link'],
      },
    })
    expect(wrapper.text()).toContain('Elige tu Rol')
  })

  it('renders all 5 role cards with correct display names', () => {
    const wrapper = mount(RoleSelection, {
      global: {
        stubs: ['router-link'],
      },
    })
    for (const name of ROLE_NAMES) {
      expect(wrapper.text()).toContain(name)
    }
  })

  it('renders difficulty labels for all roles', () => {
    const wrapper = mount(RoleSelection, {
      global: {
        stubs: ['router-link'],
      },
    })
    for (const diff of DIFFICULTIES) {
      expect(wrapper.text()).toContain(diff)
    }
  })

  it('renders "Seleccionar" button for each role', () => {
    const wrapper = mount(RoleSelection, {
      global: {
        stubs: ['router-link'],
      },
    })
    const buttons = wrapper.findAll('button')
    const selectButtons = buttons.filter(b => b.text() === 'Seleccionar')
    expect(selectButtons).toHaveLength(5)
  })

  it('renders "Volver" button', () => {
    const wrapper = mount(RoleSelection, {
      global: {
        stubs: ['router-link'],
      },
    })
    expect(wrapper.text()).toContain('Volver')
  })

  it('shows stat deltas for each role', () => {
    const wrapper = mount(RoleSelection, {
      global: {
        stubs: ['router-link'],
      },
    })
    // Sherpa has +15 stamina
    expect(wrapper.text()).toContain('+15')
    // Clasico has +5 HP
    expect(wrapper.text()).toContain('+5')
    // Investigador has -10 HP
    expect(wrapper.text()).toContain('-10')
  })

  it('calls newGame with correct role when a role is selected', async () => {
    const mockNewGame = vi.mocked(gameApi.newGame)
    mockNewGame.mockResolvedValue({
      session_id: 'test-123',
      state: {
        session_id: 'test-123',
        status: 'ALIVE',
        turn: 0,
        player: { hp: 110, stamina: 120, body_temp: 37, willpower: 105, altitude: 5200, max_altitude_reached: 5200, turns_above_8000: 0, entered_death_zone: false },
        consumables: { food_rations: 10, gas_canisters: 5, rope_sections: 3, oxygen_pct: 100 },
        weather: 'CLEAR',
        weather_forecast: 'CLEAR',
        forecast_reliability: 1.0,
        route_secured: 0,
        death_cause: null,
        narrative_log: [],
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
        role: 'sherpa',
        free_heal_used: false,
      },
      narrative: 'Welcome',
      role_display_name: 'Sherpa',
      role_difficulty: 'Easy',
    })

    const wrapper = mount(RoleSelection, {
      global: {
        stubs: ['router-link'],
        plugins: [createPinia()],
      },
    })

    // Click the first "Seleccionar" button (Sherpa)
    const selectButtons = wrapper.findAll('button').filter(b => b.text() === 'Seleccionar')
    await selectButtons[0].trigger('click')

    // Wait for async operations
    await wrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 50))

    expect(mockNewGame).toHaveBeenCalledWith('sherpa')
  })
})
