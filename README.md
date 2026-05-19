# MORS ☠️

> *Non Omnis Moriar — No Todo de Mí Morirá*

Roguelike de supervivencia en alta montaña basado en turnos. El jugador intenta escalar el K2 (8.611m) gestionando recursos físicos y psicológicos contra un motor climático impredecible. Cada turno representa una hora de expedición. No hay guardado automático. No hay segunda oportunidad.

---

## ️ Características

- **Motor matemático puro** — `f(GameState, Action) → (GameState, TurnDeltas)`, sin I/O ni estado mutable
- **Sistema climático Markov** — 5 estados climáticos con transiciones probabilísticas y forecast ruidoso (~25% de error)
- **Eventos aleatorios** — 10 tipos de eventos (avalanchas, alucinaciones, edema pulmonar, segundo viento...)
- **Psicología mecánica** — Willpower afecta la UI, las tasas de pérdida y el texto narrativo
- **Zona de la Muerte** — ≥8000m intensifica todos los efectos negativos
- **Narrativa contextual** — Templates que varían por altitud, clima, willpower y acción
- **Deltas explícitos** — El backend devuelve cambios por atributo para animaciones frontend

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Backend | FastAPI + Python 3.12 + Pydantic |
| Frontend | Vue 3 + Vite + Pinia + TypeScript |
| Estilos | TailwindCSS v4 |
| Estado (MVP) | Dict en memoria |
| Tests | Pytest (backend) + vue-tsc (frontend) |

---

## 📦 Estructura del Proyecto

```
MORS/
├── mors-backend/              # Backend FastAPI
│   ├── app/
│   │   ├── core/              # Engine puro + Markov weather
│   │   ├── models/            # Pydantic models (GameState, enums)
│   │   ├── schemas/           # API request/response schemas
│   │   ├── repositories/      # Session storage (Protocol + Memory)
│   │   ├── services/          # Game, event, narrative, session
│   │   └── routers/           # REST endpoints
│   └── tests/                 # Unit + integration tests
├── mors-frontend/             # Frontend Vue 3
│   ├── src/
│   │   ├── api/               # Fetch wrapper + TypeScript types
│   │   ├── stores/            # Pinia stores (game, ui)
│   │   ├── composables/       # useGameLoop, useAnimatedStats
│   │   ├── views/             # MainMenu, GameView, SummitView, GameOver
│   │   └── components/        # HUD, gameplay, narrative, shared
│   └── package.json
├── mvp.md                     # Documento de diseño completo
└── AGENTS.md                  # Instrucciones para agentes
```

---

## 🚀 Inicio Rápido

### Prerrequisitos

- **Python 3.12** (vía Homebrew en macOS: `brew install python@3.12`)
- **Node.js ≥20.19.0**

> ⚠️ Python 3.14+ no es compatible con pydantic-core. Usar Python 3.12.

### Backend

```bash
# Crear entorno virtual con Python 3.12
/opt/homebrew/bin/python3.12 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r mors-backend/requirements.txt

# Levantar servidor con hot-reload
PYTHONPATH=mors-backend uvicorn app.main:api --reload --port 8000
```

El servidor corre en `http://localhost:8000`. Documentación automática en `http://localhost:8000/docs`.

### Frontend

```bash
cd mors-frontend
npm install
npm run dev          # http://localhost:5173
```

---

## 🎮 Reglas de Negocio

### Atributos del Jugador

| Atributo | Rango | Inicio | Descripción |
|---|---|---|---|
| HP | 0–100 | 100 | Vida. Si llega a 0, muerte |
| Stamina | 0–100 | 100 | Energía para acciones |
| Body Temp | 0–42°C | 37.0°C | Hipotermia si <35°C |
| Willpower | 0–100 | 100 | Resistencia mental |
| Altitude | 5200–8611m | 5200m | Progreso de escalada |

### Acciones

| Acción | Efecto | Costo |
|---|---|---|
| Avanzar | +150m | Stamina moderada |
| Avanzar Agresivo | +280m, riesgo de caída | Stamina alta |
| Asegurar Ruta | Protege próximos 3 turnos | 1 cuerda + stamina |
| Acampar | Recupera stamina/temp | 1 comida + 1 gas |
| Usar Oxígeno | Recupera O₂ + willpower | 1 gas canister |
| Comer | Recupera stamina leve | 1 ración |
| Descender | -200m, mejora temp | Stamina mínima |
| Descansar | Recupera stamina en ruta | Willpower leve |

### Fórmula de Stamina

```
costo = 15 × (1 + (altitud / 8000)²) × weather_mod × oxygen_mod × willpower_mod
```

- `weather_mod`: CLEAR=1.0, CLOUDY=1.2, WIND=1.5, STORM=2.0, WHITEOUT=3.0
- `oxygen_mod`: >50% O₂ → 0.8, <30% → 1.4
- `willpower_mod`: <20 → 1.15

### Condiciones de Victoria/Derrota

- **Victoria:** Altitud ≥ 8611m con HP > 0
- **Derrota:** HP ≤ 0
  - `DEAD_EXHAUSTION` — Stamina agotada
  - `DEAD_COLD` — Hipotermia (temp <35°C)
  - `DEAD_FALL` — Caída en avance agresivo
  - `DEAD_STORM` — Tormenta fatal
  - `DEAD_EDEMA` — Edema pulmonar

---

## 🧪 Testing

### Backend

```bash
PYTHONPATH=mors-backend .venv/bin/python -m pytest mors-backend/tests/ -v
```

**100 tests passing:**
- 52 unit tests (engine, weather, events)
- 27 integration tests (API endpoints)
- 15 playability tests (summit/death reachable)

### Frontend

```bash
cd mors-frontend
npm run type-check   # vue-tsc
npm run build        # production build
```

---

## 📖 Documentación

- `mvp.md` — Documento de diseño completo con todos los requerimientos funcionales
- `mors-backend/README.md` — Arquitectura backend, reglas de negocio, API contracts
- `mors-frontend/README.md` — Arquitectura frontend, reglas de presentación, routing
- `AGENTS.md` — Instrucciones para agentes de desarrollo

---

## 🏗️ Arquitectura

### Principios

1. **Engine puro** — Sin I/O, sin estado mutable externo. 100% testeable en aislamiento
2. **Deltas explícitos** — El backend devuelve cambios por atributo. Frontend anima sin recalcular
3. **El pronóstico miente** — `weather` (real) vs `weather_forecast` (ruidoso ~25%)
4. **Narrativa desacoplada** — El motor matemático no sabe nada de la IA narrativa
5. **Repository pattern** — `AbstractSessionRepository` permite migrar memoria → Redis sin tocar el engine

### Flujo de un Turno

```
Usuario → ActionPanel → ConfirmModal (si costosa)
    ↓
useGameLoop → POST /game/turn {session_id, action}
    ↓
GameService → SessionRepository.get()
    ↓
GameEngine.process(state, action) → TurnResult
    ↓
EventService.roll() → RandomEvent | None
    ↓
NarrativeService.generate() → texto contextual
    ↓
SessionRepository.save() → TurnResponse
    ↓
gameStore actualiza → componentes re-renderizan
```

---

## 📝 Licencia

Proyecto educativo. Sin licencia formal.

---

## 🙏 Créditos

Inspirado en la escalada del K2 y la literatura de supervivencia en alta montaña.

> *"La montaña no te ve. No le importas. Y sin embargo, aquí estás."*
