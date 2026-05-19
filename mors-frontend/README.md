# MORS Frontend

Vue 3 + Pinia + TailwindCSS frontend para MORS — roguelike de supervivencia en alta montaña.

---

## Propósito

Interfaz de juego reactiva que consume el backend FastAPI. Gestiona estado de partida, animaciones de stats, panel de acciones y log narrativo. Toda la lógica de negocio vive en el backend; el frontend solo renderiza y pasa acciones.

**Stack:** Vue 3 + Vite + Pinia + TailwindCSS + TypeScript

---

## Arquitectura

```
API (fetch POST /game/turn)
    ↓
gameStore (Pinia) — estado reactivo global
    ↓
composables (useGameLoop, useAnimatedStats)
    ↓
views / components
    ↓
Template Vue → DOM
```

---

## Reglas de Presentación

### RF-10 — Interfaz de Usuario

**Stats siempre visibles (3 columnas en desktop ≥1024px):**

- Columna izquierda: `StatsPanel`, `AltitudeIndicator`, `WeatherWidget`
- Columna central: `NarrativeLog`, `ResourceGrid`
- Columna derecha: `ActionPanel`

**Barras de stats (StatBar):**
- Color semántico: HP=danger, Stamina=warning, Temp=glacier/normal/success, Willpower=peak
- Temperatura usa óptimal=37°C → verde si ≈37, rojo si se aleja
- Transición animada de 500ms en cambios de ancho

**Altitud (AltitudeIndicator):**
- Barra vertical 5200m → 8611m
- Zona de la Muerte marcada en rojo desde 8000m
- Indicador de posición actual

**Clima (WeatherWidget):**
- Icono por estado (☀️ ☁️ 💨 ⛈️ 🌫️)
- Clima real + pronóstico + % fiabilidad
- Color del fiabilidad: >80% verde, 50-80% warning, <50% danger

### RF-10.5 — Animación de Deltas

Los cambios de atributos se animan con `useAnimatedStats`:
- Duración: 600ms
- Easing: cubic ease-out `1 - (1 - t)³`
- DeltaIndicator: verde para +, rojo para −

### RF-10.11 — Estados DOUBT y DESPAIR

Cuando `willpower < 30` (estado DOUBT) y `willpower < 15` (DESPAIR):
- El texto de los botones cambia a "¿Seguir...?"
- Tipografía más tenue
- Sin cambios dramáticos en layout (el backend maneja la narrativa)

### RF-10.12 — Ciclo Día/Noche en UI

- `turn % 24 >= 12` → turno nocturno
- Indicador 🌙/☀️ en `TurnCounter`
- `isNight` calculado en `gameStore` y pasado a componentes

### RF-10.10 — Death Zone Visual

Cuando `altitude >= 8000m`:
- Background de GameView cambia de `bg-mors` a `bg-peak` (más frío)
- `inDeathZone` computed en `gameStore`

---

## Flujo de Datos

### Inicio de Partida

```
MainMenu → useGameLoop.startOrResume()
    ↓ localStorage check
    ├─ session_id existe → gameStore.resumeGame(id) → GET /game/state/{id}
    └─ no existe → gameStore.startGame() → POST /game/new
    ↓
router.push('/game')
```

### Turno

```
ActionPanel (click) → useGameLoop.executeAction(action)
    ↓ acciones costosas (ADVANCE_AGGRESSIVE, SECURE_ROUTE, CAMP)
    ├─ openConfirm() → ConfirmModal visible
    └─ direct → gameStore.takeTurn(action) → POST /game/turn
    ↓
gameStore se actualiza con TurnResponse
    ↓
App.vue watch(status) → router.push('/summit' | '/gameover')
```

---

## Estructura de Archivos

```
mors-frontend/
├── src/
│   ├── main.ts                    # createApp + Pinia + Router
│   ├── App.vue                    # RouterView + watch status → navegación automática
│   ├── api/
│   │   ├── types.ts               # GameState, TurnDeltas, ActionType, etc.
│   │   └── game.ts                # newGame, postTurn, getState, deleteSession
│   ├── stores/
│   │   ├── gameStore.ts           # estado reactivo, acciones, computed (status/altitude/willpowerState…)
│   │   └── uiStore.ts             # confirmModal, eventBanner
│   ├── composables/
│   │   ├── useGameLoop.ts         # startOrResume, executeAction, confirmAction
│   │   └── useAnimatedStats.ts     # RAF interpolation de deltas
│   ├── views/
│   │   ├── MainMenu.vue           # Nueva Partida / Continuar
│   │   ├── GameView.vue           # Layout 3 columnas, muerte zona, routing
│   │   ├── SummitView.vue         # Victoria
│   │   └── GameOver.vue           # Derrota + epitafio
│   └── components/
│       ├── hud/
│       │   ├── StatsPanel.vue         # HP / Stamina / Temp / Willpower
│       │   ├── AltitudeIndicator.vue  # Barra vertical + zona de muerte
│       │   ├── WeatherWidget.vue     # Clima + forecast + fiabilidad
│       │   └── TurnCounter.vue     # Turno + indicador día/noche
│       ├── gameplay/
│       │   ├── ActionPanel.vue     # Botones de acciones con DOUBT state
│       │   ├── ResourceGrid.vue    # Comida / Gas / Cuerda / O₂
│       │   └── EventBanner.vue      # Notificación de evento aleatorio
│       ├── narrative/
│       │   └── NarrativeLog.vue   # Bitácora con scroll
│       └── shared/
│           ├── StatBar.vue         # Barra reutilizable con color semántico
│           ├── DeltaIndicator.vue # Número animado +/-
│           └── ConfirmModal.vue   # Modal de confirmación
├── vite.config.ts                 # Vue + Tailwind (@tailwindcss/vite plugin)
└── src/assets/main.css            # @import "tailwindcss" + @theme custom colors
```

---

## Tailwind Theme — Colores Custom

```css
@theme {
  --color-snow: #f0f4f8;
  --color-ice: #c8d6e5;
  --color-glacier: #74b9ff;
  --color-peak: #2d3436;
  --color-danger: #e74c3c;
  --color-warning: #f39c12;
  --color-success: #27ae60;
  --color-mors: #1a1a2e;
  --color-death-zone: #c0392b;
}
```

| Color | Uso |
|---|---|
| `snow` | Texto principal sobre fondo oscuro |
| `ice` | Texto secundario, labels |
| `glacier` | Acento primario, elementos interactivos |
| `peak` | Background alternativo (death zone) |
| `mors` | Background principal |
| `danger` | HP bajo, alertas críticas |
| `warning` | Stamina, fiabilidad media |
| `success` | HP óptimo, fiabilidad alta |
| `death-zone` | Warning de 8000m+ |

---

## Routing

| Path | Componente | Condición |
|---|---|---|
| `/` | MainMenu | Siempre accesible |
| `/game` | GameView | Session activa |
| `/summit` | SummitView | `status === 'SUMMIT'` (auto-navega) |
| `/gameover` | GameOver | `status === 'DEAD'` (auto-navega) |

App.vue tiene un `watch` sobre `game.status` que navega automáticamente cuando el juego termina.

---

## API — Integración con Backend

**Base URL:** `http://localhost:8000`

Todas las funciones en `api/game.ts` usan `fetch` vanilla. Errores lanzan `Error` con `detail` del response JSON.

```ts
// Iniciar partida
newGame(): Promise<{ session_id, state, narrative }>

// Procesar turno
postTurn({ session_id, action }): Promise<TurnResult>

// Consultar estado
getState(sessionId): Promise<{ state: GameState }>

// Eliminar sesión
deleteSession(sessionId): Promise<void>
```

**Manejo de errores en stores:**
- `game.isLoading` bloquea acciones mientras el server procesa
- `game.error` se muestra en la UI (Actualmente solo logged en consola)
- Retry logic: no implementada en MVP — se depende de `game.isLoading` para evitar doble envío

---

## Configuración de Ambiente

El frontend asume el backend en `http://localhost:8000`. Para cambiar:
- Editar `API_BASE` en `src/api/game.ts`

---

## Desarrollo

```bash
cd mors-frontend
npm install
npm run dev        # http://localhost:5173 con HMR
npm run build       # production build en dist/
npm run type-check # vue-tsc --build
```

**Requisitos:** Node.js ≥20.19.0

---

## Decisiones de Diseño Registradas

- **Tailwind v4** con `@tailwindcss/vite` plugin (no postcss + autoprefixer legacy)
- **Tailwind theme via `@theme`** en CSS — no `tailwind.config.js`
- **Pinia** para estado reactivo (no Vuex, no provide/inject para estado global)
- **No axios** — fetch nativo + thin wrapper en `api/game.ts`
- **No router guards** — la navegación es driven por estado del store (watch en App.vue)
- **DeltaIndicator usa RAF manual** — no libraries de animación