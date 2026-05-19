# MORS — Agent Instructions

## Proyecto

MORS — Roguelike de supervivencia en alta montaña (K2, 8611m). Backend FastAPI + Frontend Vue 3.

---

## Comandos Principales

### Backend (mors-backend)

```bash
# Tests unitarios (desde root del repo)
PYTHONPATH=mors-backend .venv/bin/python -m pytest mors-backend/tests/unit/ -v

# Levantar server con hot-reload
PYTHONPATH=mors-backend .venv/bin/uvicorn app.main:api --reload --port 8000

# Verificación de imports
PYTHONPATH=mors-backend .venv/bin/python -c "from app.main import api"
```

> ⚠️ El `.venv` en root fue creado con **Python 3.12** (`/opt/homebrew/bin/python3.12`). Si el interpreter es 3.14+ (el default del sistema), pydantic-core no compila — hay que usar el venv con Python 3.12.

### Frontend (mors-frontend)

```bash
cd mors-frontend
npm install          # primero, tras clon
npm run dev          # http://localhost:5173
npm run build        # producción
npm run type-check   # vue-tsc --build
```

> ⚠️ **Tailwind v4** — NO usa `tailwind.config.js` legacy. Configuración vía `@tailwindcss/vite` plugin + `@import "tailwindcss"` + `@theme {}` en CSS. Si agregas colors, van en `src/assets/main.css` bajo `@theme {}`, no en un archivo de configuración separado.

---

## Arquitectura

### Backend (`mors-backend/`)

- **Entry point:** `app/main.py` — FastAPI con CORS y lifespan
- **Engine puro:** `app/core/game_engine.py` — `f(GameState, Action) → (GameState, TurnDeltas)`, sin I/O
- **Weather:** `app/core/markov_weather.py` — cadena de Markov con forecast ruidoso
- **Models:** `app/models/game_state.py`, `app/models/enums.py`
- **Schemas:** `app/schemas/game.py`
- **Repositories:** `app/repositories/base.py` (Protocol) → `app/repositories/memory_repo.py` (MVP singleton)
- **Services:** `app/services/game_service.py`, `event_service.py`, `narrative_service.py`, `session_service.py`
- **Routers:** `app/routers/game.py`, `app/routers/session.py`

### Frontend (`mors-frontend/`)

- **Estado global:** Pinia (`gameStore.ts`, `uiStore.ts`)
- **Motor de turnos:** `composables/useGameLoop.ts`
- **Navegación:** watch en `App.vue` sobre `game.status` → auto-route a `/summit` o `/gameover`
- **API client:** `src/api/game.ts` — fetch wrapper, assume BE en `http://localhost:8000`
- **Tipos:** `src/api/types.ts` — todos los tipos TypeScript del dominio

### Contracto clave: Deltas

El backend devuelve `TurnDeltas` en cada respuesta. El frontend los usa para animaciones. No recalcular valores en el frontend — usar lo que devuelve el server.

---

## Reglas de Negocio Críticas

- **Altitud inicial:** 5200m. **Cima:** 8611m. **Zona de la Muerte:** ≥8000m
- **Stamina cost:** `15 × (1 + (alt/8000)²) × weather_mod × oxygen_mod × willpower_mod`
- **Weather modifiers:** CLEAR=1.0, CLOUDY=1.2, WIND=1.5, STORM=2.0, WHITEOUT=3.0
- **Noche (turno % 24 >= 12):** penalty 1.3×, forecast reliability −0.10
- **Willpower < 20:** +15% stamina cost (jugador se arrastra mentalmente)
- **HP llega a 0:** muerte. Causa según contexto (DEAD_EXHAUSTION, DEAD_COLD, DEAD_FALL…)
- **Un evento por turno máximo.** SECOND_WIND solo si 10+ turnos sin recuperar stamina
- **El forecast miente ~25%** — `forecast_reliability` reduce esa chance con altitud y noche

---

## Convenciones

- **TypeScript frontend:** `noUncheckedIndexedAccess: true` en tsconfig — accesos a array/obj pueden ser `undefined`, verificar
- **Python datetime:** usar `datetime.now(timezone.utc)` — NO `datetime.utcnow()` (deprecated)
- **Session management:** session_id en `localStorage` bajo key `mors_session_id`
- **Pinia store en composables:** `useGameLoop` inyecta stores explícitamente — no hace `useStore()` sin argumento
- **ConfirmModal:** se abre desde `useGameLoop.executeAction()` para acciones costosas
- **Tailwind custom colors:** `snow`, `ice`, `glacier`, `peak`, `danger`, `warning`, `success`, `mors`, `death-zone`

---

## Fuentes

- Diseño completo: `mvp.md` (root)
- Backend: `mors-backend/README.md`
- Frontend: `mors-frontend/README.md`