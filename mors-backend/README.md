# MORS Backend

FastAPI backend para MORS — roguelike de supervivencia en alta montaña.

---

## Propósito

Backend que gestiona la lógica de juego pura: motor de turnos, sistema climático con Markov, eventos aleatorios y generación narrativa. No tiene estado mutable externo — el motor es una función pura `f(GameState, Action) → (GameState, TurnDeltas)`.

**Stack:** FastAPI + Pydantic + Python 3.12+

---

## Arquitectura

```
Request HTTP
    ↓
Router (game.py / session.py)
    ↓
Service (GameService / SessionService)
    ↓
Repository (MemorySessionRepository)
    ↓
Core (game_engine.py / markov_weather.py)
    ↓
Models (Pydantic BaseModels)
```

Los servicios orquestan. El engine y Markov son puros — sin I/O, sin estado mutable.

---

## Reglas de Negocio

### RF-05 — Motor Matemático

**Costo de Stamina por acción:**

```
stamina_cost = BASE × (1 + (altitud / 8000)²) × weather_mod × oxygen_mod × willpower_mod
```

- `BASE = 15.0`
- `oxygen_mod`: >50% → 0.8, <30% → 1.4, resto → 1.0
- `willpower_mod`: <20 → 1.15, resto → 1.0

**Caída en Avanzar Agresivo:**

```
p_caida = 0.05 + max(0, (100 - stamina) / 100 × 0.3) × weather_mod × (1 - route_secured × 0.1)
```

**Temperatura corporal pasiva (por turno):**

```
temp_delta = -(0.1 + altitud_factor × 0.05 + (weather_mod-1) × 0.1 + night × 0.2 - secured × 0.02)
```

**Willpower pasivo (por turno):**

```
willpower_delta = -(0.5 + altitud_factor × 0.1 + night × 0.3 + turns_above_8000 × 0.15)
```

### RF-06 — Sistema Climático

**Matrix de transiciones Markov** — cada estado tiene distribución probabilística sobre el próximo:

| Desde ↓ / Hacia → | CLEAR | CLOUDY | WIND | STORM | WHITEOUT |
|---|---|---|---|---|---|
| CLEAR | 0.60 | 0.25 | 0.10 | 0.04 | 0.01 |
| CLOUDY | 0.20 | 0.50 | 0.20 | 0.08 | 0.02 |
| WIND | 0.10 | 0.25 | 0.40 | 0.20 | 0.05 |
| STORM | 0.05 | 0.15 | 0.35 | 0.35 | 0.10 |
| WHITEOUT | 0.02 | 0.08 | 0.20 | 0.40 | 0.30 |

**Weather modifiers:** CLEAR=1.0, CLOUDY=1.2, WIND=1.5, STORM=2.0, WHITEOUT=3.0

**Pronóstico ruidoso:** `forecast_reliability` se reduce con altitud (>7000m), noche (-0.10) y tormentas (-0.10). Cuando reliability < 1.0, el forecast tiene ~25% de probabilidad de ser incorrecto.

### RF-07 — Eventos Aleatorios

Probabilidad base: `0.15 + turns_above_8000 × 0.05` (max 0.50).

| Evento | Efecto | Condición |
|---|---|---|
| DISTANT_AVALANCHE | Willpower −15 | siempre |
| HALLUCINATION | Willpower −20 | siempre |
| WIND_GUST | Stamina −15 | siempre |
| O2_REGULATOR_FAIL | O₂ → 0, gas −1 | siempre |
| FROSTBITE | HP −10, temp −2°C | siempre |
| PULMONARY_EDEMA | HP −20, Stamina −30 | >8000m |
| TENT_COLLAPSE | Stamina −25, temp −3°C | siempre |
| PARTNER_VISION | Willpower −5 | siempre |
| EQUIPMENT_DROP | cuerda o ración −1 | siempre |
| SECOND_WIND | Stamina +20, Willpower +10 | 10 turnos sin recuperar stamina |

Solo ocurre **un evento por turno máximo**.

### RF-08 — Willpower y Estados Psicológicos

- `WILLPOWER < 30` → estado **DOUBT**: texto dubitativo en botones ("¿Seguir...?")
- `WILLPOWER < 15` → estado **DESPAIR**: aumenta probabilidad de HALLUCINATION
- `WILLPOWER = 0` → tasa de pérdida de HP por agotamiento se **duplica**
- Primera vez cruzando 8000m → bonus +25 Willpower (una vez)

### RF-09 — Condiciones de Terminal

- **Victoria:** altitud ≥ 8611m con HP > 0 → status = `SUMMIT`
- **Derrota:** HP ≤ 0 → status = `DEAD`, death_cause según causa
  - `DEAD_EXHAUSTION`: HP llegó a 0 por stamina agotada
  - `DEAD_COLD`: HP llegó a 0 por hipotermia (temp < 35°C)
  - `DEAD_FALL`: triggered por caída en avance agresivo
  - `DEAD_STORM`: tormenta fatal (WHITEOUT)
  - `DEAD_EDEMA`: pulmonary edema

### RF-03 — Ciclo Día/Noche

Turno % 24:
- **Día (0–11):** penalty 1.0×, forecast_reliability no penalizado por noche
- **Noche (12–23):** penalty 1.3×, forecast_reliability −0.10, temp extra −0.2°C

---

## API Endpoints

| Método | Path | Descripción |
|---|---|---|
| `POST` | `/game/new` | Crea nueva sesión, devuelve estado inicial + narrativa |
| `POST` | `/game/turn` | Procesa un turno `{session_id, action}` → TurnResponse |
| `GET` | `/game/state/{session_id}` | Consulta estado sin modificar |
| `DELETE` | `/game/session/{session_id}` | Elimina sesión |
| `GET` | `/game/sessions` | Lista sesiones activas (dev) |
| `GET` | `/health` | Health check |

---

## Contratos de Datos

### TurnResponse

```json
{
  "new_state": { /* GameState completo */ },
  "deltas": {
    "hp_delta": 0.0,
    "stamina_delta": -17.07,
    "temp_delta": -0.15,
    "willpower_delta": -1.5,
    "altitude_delta": 150.0,
    "oxygen_delta": 0.0,
    "route_secured_delta": 0
  },
  "event": { "event_type": "...", "narrative": "..." } | null,
  "narrative": "Avanzas con paso firme...",
  "is_terminal": false
}
```

### GameState (referencia completa en `app/models/game_state.py`)

Campos clave: `session_id`, `status` (ALIVE/DEAD/SUMMIT/ABANDONED), `turn`, `player` (hp/stamina/body_temp/willpower/altitude/max_altitude_reached/turns_above_8000), `consumables` (food/gas/rope/oxygen), `weather`, `weather_forecast`, `forecast_reliability`, `route_secured`, `death_cause`, `narrative_log`, `turns_without_stamina_recovery`.

---

## Configuración

Variables de entorno (`.env.example`):

```env
APP_NAME=MORS API
DEBUG=true
NARRATIVE_MODE=local
ANTHROPIC_API_KEY=
SESSION_TTL_HOURS=6
```

- `NARRATIVE_MODE=local` → templates. `NARRATIVE_MODE=anthropic` → API de Anthropic (fallback a local si falla o timeout 1.5s).
- `SESSION_TTL_HOURS` → TTL de sesiones en memoria.

---

## Patrones de Arquitectura

### Repository Pattern

`AbstractSessionRepository` es un Protocol. `MemorySessionRepository` es la implementación MVP (dict en memoria, singleton). Para migrar a Redis: crear `RedisSessionRepository` implementando el mismo Protocol, cambiar un import. El engine no se toca.

### Service Layer

Los servicios orquestan I/O y llamdas al engine. El engine es agnóstico de cómo se persiste o se serializa.

### Deltas Explícitos

Cada respuesta de turno incluye los `deltas` de cada atributo. El frontend los usa para animaciones. El backend es la única fuente de verdad.

---

## Testing

```bash
PYTHONPATH=mors-backend .venv/bin/python -m pytest mors-backend/tests/unit/ -v
```

- **34 tests passing** — coverage del engine ≥ 80%
- `test_game_engine.py`: todas las fórmulas puras, acciones, condiciones de victoria/derrota
- `test_markov_weather.py`: matriz de transiciones, forecast ruidoso, reliability

---

## Desarrollo

```bash
# Crear venv con Python 3.12
/opt/homebrew/bin/python3.12 -m venv .venv
source .venv/bin/activate
pip install -r mors-backend/requirements.txt

# Levantar server con hot-reload
PYTHONPATH=mors-backend .venv/bin/uvicorn app.main:api --reload --port 8000
```

El server corre en `http://localhost:8000`. Documentación automática en `http://localhost:8000/docs`.

---

## Estructura de Archivos

```
mors-backend/
├── app/
│   ├── main.py                 # FastAPI app, CORS, routers
│   ├── core/
│   │   ├── config.py          # Settings (pydantic-settings)
│   │   ├── game_engine.py     # f(GameState, Action) → (GameState, TurnDeltas)
│   │   └── markov_weather.py  # cadena de Markov + forecast ruidoso
│   ├── models/
│   │   ├── enums.py          # ActionType, WeatherState, DeathCause, SessionStatus, EventType
│   │   └── game_state.py     # PlayerStats, Consumables, GameState, TurnDeltas, TurnResult, RandomEvent
│   ├── schemas/
│   │   └── game.py           # NewGameResponse, TurnRequest, TurnResponse, StateResponse
│   ├── repositories/
│   │   ├── base.py           # AbstractSessionRepository (Protocol)
│   │   └── memory_repo.py    # Dict en memoria (singleton)
│   ├── services/
│   │   ├── game_service.py   # orquestación completa
│   │   ├── event_service.py # eventos aleatorios
│   │   ├── narrative_service.py  # templates + epitafio
│   │   └── session_service.py # CRUD sesiones + TTL
│   └── routers/
│       ├── game.py           # POST /game/new, /turn, GET /state/{id}
│       └── session.py        # DELETE /session/{id}, GET /sessions
├── tests/
│   ├── unit/
│   │   ├── test_game_engine.py
│   │   └── test_markov_weather.py
│   └── integration/
├── requirements.txt
└── .env.example
```