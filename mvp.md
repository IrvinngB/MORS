# MORS ☠️
### *Non Omnis Moriar — No Todo de Mí Morirá*

Roguelike de supervivencia en alta montaña basado en turnos. El jugador intenta escalar el K2 (8.611m) gestionando recursos físicos y psicológicos contra un motor climático impredecible. Cada turno representa una hora de expedición. No hay guardado automático. No hay segunda oportunidad.

> **MORS** es el nombre definitivo del proyecto. El título en pantalla puede alternar entre `MORS` y el subtítulo latino según contexto narrativo.

---

## Stack Tecnológico

| Capa | Tecnología | Justificación |
|---|---|---|
| Backend | FastAPI (Python 3.12+) | Async nativo, validación Pydantic, ideal para lógica de turnos |
| Frontend | Vue 3 + Vite | Reactividad fina con Pinia, ideal para HUD de stats en tiempo real |
| Estilos | TailwindCSS | Utilidades sin overhead, personalizable para estética oscura |
| Estado del juego (MVP) | Dict en memoria | Suficiente para validar mecánica sin dependencias externas |
| Estado (producción) | Redis + TTL | Persistencia horizontal sin tocar el engine |
| Narrativa IA | Anthropic API (claude-sonnet) | Generación contextual de texto narrativo por turno |
| Comunicación | REST (HTTP/JSON) | Simple, predecible, compatible con polling de estado |
| Tests | Pytest (backend) + Vitest (frontend) | Cobertura unitaria del motor matemático ≥ 80% |

---

## Arquitectura del Proyecto

### Principios Arquitectónicos

1. **Engine puro**: `game_engine.py` es una función pura — `f(GameState, Action) → (GameState, TurnDeltas)`. Sin I/O, sin estado mutable externo. 100% testeable en aislamiento.
2. **Deltas explícitos**: El backend no solo devuelve el nuevo estado — devuelve los deltas de cada atributo. El frontend anima los cambios sin recalcular nada.
3. **El pronóstico miente**: El backend mantiene `weather` (real) y `weather_forecast` (lo que ve el jugador, incorrecto ~25% de las veces). La tensión nace de esa información incompleta.
4. **Narrativa desacoplada**: El motor matemático no sabe nada de la IA narrativa. El `NarrativeService` consume el `TurnResult` y genera texto de forma asíncrona y opcional.
5. **Sesiones en memoria para MVP**: Un `dict[session_id → GameState]` valida la mecánica. La abstracción del `SessionRepository` permite migrar a Redis sin tocar el engine.

---

### Backend — FastAPI

```
mors-backend/
├── app/
│   ├── main.py                      # Monta la app, registra routers, configura CORS y lifespan
│   ├── core/
│   │   ├── config.py                # Settings con pydantic-settings (.env)
│   │   ├── game_engine.py           # Motor matemático puro — f(GameState, Action) → (GameState, TurnDeltas)
│   │   └── markov_weather.py        # Cadena de Markov climática — genera transiciones y forecast con ruido
│   ├── models/
│   │   ├── game_state.py            # GameState, PlayerStats, Consumables (Pydantic BaseModel)
│   │   ├── enums.py                 # ActionType, WeatherState, DeathCause, SessionStatus, EventType
│   │   └── turn_result.py           # TurnResult: nuevo estado + deltas + eventos + narrativa
│   ├── schemas/
│   │   └── game.py                  # NewGameResponse, TurnRequest, TurnResponse, StateResponse
│   ├── repositories/
│   │   ├── base.py                  # AbstractSessionRepository (Protocol)
│   │   └── memory_repo.py           # Dict en memoria — implementación MVP
│   ├── services/
│   │   ├── game_service.py          # Orquestación: recupera sesión → engine → eventos → persiste
│   │   ├── event_service.py         # Eventos aleatorios: avalanchas, alucinaciones, fallos de equipo
│   │   ├── narrative_service.py     # Generación de texto narrativo (local + Anthropic API opcional)
│   │   └── session_service.py       # CRUD de sesiones + expiración TTL
│   └── routers/
│       ├── game.py                  # POST /game/new, POST /game/turn, GET /game/state/{id}
│       └── session.py               # DELETE /game/session/{id}, GET /game/sessions (dev)
├── tests/
│   ├── unit/
│   │   ├── test_game_engine.py      # Tests de fórmulas puras — cobertura ≥ 80%
│   │   ├── test_markov_weather.py   # Tests de distribución de transiciones climáticas
│   │   └── test_event_service.py    # Tests de probabilidades de eventos
│   └── integration/
│       └── test_api.py              # Tests de endpoints con TestClient
├── requirements.txt
├── requirements-dev.txt
└── .env.example
```

#### Contratos de datos clave

```python
# models/game_state.py
class PlayerStats(BaseModel):
    hp: float                      # 0–100
    stamina: float                 # 0–100
    body_temp: float               # Celsius, inicia en 37.0
    willpower: float               # 0–100
    altitude: float                # metros, inicia en 5200

class Consumables(BaseModel):
    food_rations: int              # unidades
    gas_canisters: int             # unidades
    rope_sections: int             # unidades
    oxygen_pct: float              # 0–100

class GameState(BaseModel):
    session_id: str                # UUID v4
    status: SessionStatus          # ALIVE | DEAD | SUMMIT | ABANDONED
    turn: int                      # turno actual (hora de expedición)
    player: PlayerStats
    consumables: Consumables
    weather: WeatherState          # clima real (oculto al jugador)
    weather_forecast: WeatherState # clima visible al jugador (ruidoso)
    forecast_reliability: float    # 0.0–1.0, visible al jugador como indicador
    route_secured: int             # secciones de ruta aseguradas activas
    death_cause: DeathCause | None
    narrative_log: list[str]       # historial de texto narrativo
    created_at: datetime
    updated_at: datetime

# models/turn_result.py
class TurnDeltas(BaseModel):
    hp_delta: float
    stamina_delta: float
    temp_delta: float
    willpower_delta: float
    altitude_delta: float
    oxygen_delta: float

class TurnResult(BaseModel):
    new_state: GameState
    deltas: TurnDeltas
    event: RandomEvent | None
    narrative: str                 # texto del turno generado
    is_terminal: bool              # True si el jugador ganó o murió
```

---

### Frontend — Vue 3

```
mors-frontend/
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── api/
│   │   └── game.js                  # Fetch wrapper hacia el backend con manejo de errores
│   ├── stores/
│   │   ├── gameStore.js             # Pinia: estado reactivo de la partida
│   │   └── uiStore.js               # Pinia: estado de UI (loading, animaciones, modal confirmación)
│   ├── composables/
│   │   ├── useGameLoop.js           # Lógica de turno, loading states, errores de red
│   │   └── useAnimatedStats.js      # Interpolación animada de deltas de atributos
│   ├── views/
│   │   ├── MainMenu.vue             # Pantalla de inicio con animación de títulos
│   │   ├── GameView.vue             # Layout principal durante la partida
│   │   ├── SummitView.vue           # Pantalla de victoria con resumen de partida
│   │   └── GameOver.vue             # Pantalla de derrota con causa y altitud máxima
│   └── components/
│       ├── hud/
│       │   ├── StatsPanel.vue       # HP / Stamina / Temp / Willpower como barras animadas
│       │   ├── AltitudeIndicator.vue# Barra vertical — 5200m a 8611m — con zona de muerte marcada
│       │   ├── WeatherWidget.vue    # Clima actual + forecast + indicador de fiabilidad
│       │   └── TurnCounter.vue      # Hora de expedición + duración total
│       ├── gameplay/
│       │   ├── ActionPanel.vue      # Botones de acción con costo estimado + confirmación
│       │   ├── ResourceGrid.vue     # Comida / gas / cuerda / oxígeno como contadores
│       │   └── EventBanner.vue      # Notificación de evento aleatorio con animación de entrada
│       ├── narrative/
│       │   └── NarrativeLog.vue     # Log de eventos con scroll — historial de la sesión
│       └── shared/
│           ├── StatBar.vue          # Barra de progreso reutilizable con color semántico
│           ├── DeltaIndicator.vue   # Número animado: +N en verde / -N en rojo
│           └── ConfirmModal.vue     # Modal de confirmación para acciones irreversibles
├── public/
├── vite.config.js
└── tailwind.config.js
```

---

### Flujo de un Turno

```
Usuario presiona acción en ActionPanel.vue
            ↓
        ConfirmModal.vue (si acción costosa)
            ↓
    useGameLoop.js — bloquea UI, inicia loading
            ↓
    api/game.js → POST /game/turn { session_id, action }
            ↓
    Router → GameService
            ↓
        SessionRepository.get(session_id)
            ↓
        GameEngine.process(state, action) → TurnResult   ← función pura
            ↓
        EventService.roll(new_state) → RandomEvent | None
            ↓
        NarrativeService.generate(turn_result) → str     ← async, no bloquea el engine
            ↓
        SessionRepository.save(new_state)
            ↓
    TurnResponse { nuevo_estado, deltas, evento, narrativa }
            ↓
    gameStore.js actualiza estado reactivo
            ↓
    useAnimatedStats.js interpola deltas con animación
            ↓
    Todos los componentes re-renderizan con los nuevos valores
```

---

## Requerimientos Funcionales

### RF-01 — Gestión de Sesión

- **RF-01.1** El sistema debe generar un `session_id` único (UUID v4) al iniciar una nueva partida.
- **RF-01.2** El frontend debe persistir el `session_id` en `localStorage` para continuar sesiones activas tras recargar la página.
- **RF-01.3** El sistema debe permitir consultar el estado actual de una sesión por su `session_id` sin modificarlo.
- **RF-01.4** El sistema debe eliminar una sesión cuando el jugador confirma el abandono o la muerte.
- **RF-01.5** Las sesiones deben expirar automáticamente tras 6 horas de inactividad (TTL gestionado por `session_service`).
- **RF-01.6** Al retomar una sesión existente, el frontend debe restaurar el log narrativo completo de la sesión.
- **RF-01.7** El sistema debe registrar y devolver `turn_count`, `max_altitude_reached` y `total_play_time` para el resumen final.

### RF-02 — Estado del Jugador

- **RF-02.1** El sistema debe mantener los siguientes atributos vitales: HP, Stamina, Temperatura corporal, Willpower, Altitud actual.
- **RF-02.2** El sistema debe mantener los consumibles: Raciones de comida, Canisters de gas, Secciones de cuerda, Porcentaje de oxígeno suplementario.
- **RF-02.3** Ningún atributo de tipo porcentaje puede superar 100 ni ser inferior a 0. El engine debe clipear los valores en sus límites.
- **RF-02.4** La temperatura corporal debe modelarse en grados Celsius e iniciar en 37.0°C.
- **RF-02.5** La altitud debe iniciar en 5.200m (Campo Base Avanzado K2) y tener como objetivo 8.611m (cima).
- **RF-02.6** El sistema debe mantener un contador de `route_secured` (secciones de cuerda activas) que decrementa con los turnos.
- **RF-02.7** El sistema debe registrar la altitud máxima alcanzada en la sesión (`max_altitude_reached`) para el resumen de derrota.
- **RF-02.8** El sistema debe registrar `turns_above_8000` para intensificar los efectos de la Zona de la Muerte.

### RF-03 — Sistema de Turnos

- **RF-03.1** Cada turno representa exactamente 1 hora de expedición.
- **RF-03.2** El jugador debe elegir exactamente una acción por turno antes de que el servidor procese el resultado.
- **RF-03.3** El sistema no debe permitir acciones en sesiones con estado distinto a `ALIVE`.
- **RF-03.4** El servidor debe devolver el estado completo actualizado tras cada turno.
- **RF-03.5** El servidor debe incluir en la respuesta los deltas de cada atributo para que el frontend anime los cambios.
- **RF-03.6** El servidor debe indicar si el turno resulta en estado terminal (`is_terminal: true`) para que el frontend navegue a la pantalla correcta.
- **RF-03.7** El sistema debe simular un ciclo día/noche: turnos 0–11 son diurnos, 12–23 son nocturnos. Los turnos nocturnos aumentan la penalización de temperatura y reducen la visibilidad del pronóstico.

### RF-04 — Acciones del Jugador

- **RF-04.1** **Avanzar (Normal)**: sube ~150m, consume Stamina moderada según altitud y clima.
- **RF-04.2** **Avanzar (Agresivo)**: sube ~280m, consume Stamina alta, introduce riesgo de caída proporcional al agotamiento y al clima.
- **RF-04.3** **Asegurar Ruta**: consume una sección de cuerda y Stamina media; incrementa `route_secured` y reduce riesgo de caída durante los próximos 3 turnos.
- **RF-04.4** **Acampar**: consume comida y gas, recupera Stamina, expone a tormentas nocturnas; restaura temperatura corporal parcialmente.
- **RF-04.5** **Usar Oxígeno**: consume un canister de gas, recupera `oxygen_pct` y Willpower; reduce la penalización de altitud durante el turno actual.
- **RF-04.6** **Comer**: consume una ración, recupera Stamina y Willpower levemente; no tiene efecto si `food_rations = 0`.
- **RF-04.7** **Descender**: baja ~200m, consume Stamina mínima; mejora temperatura pasiva y reduce la presión acumulada de la Zona de la Muerte.
- **RF-04.8** **Descansar (en ruta)**: el jugador permanece en la misma altitud durante un turno. Recupera algo de Stamina y temperatura pero avanza el clima con riesgo de tormenta. Penaliza el Willpower levemente por inacción.

### RF-05 — Motor Matemático (Backend)

- **RF-05.1** El costo de Stamina por acción se calcula con la fórmula: `costo = base × (1 + (altitud / 8000)²) × weather_mod × oxygen_mod`.
- **RF-05.2** El factor de altitud es cuadrático para garantizar que el tramo 7.000–8.000m sea exponencialmente más exigente que 3.000–4.000m.
- **RF-05.3** `oxygen_mod` reduce el costo de Stamina cuando `oxygen_pct > 50`; por debajo de 30% lo incrementa.
- **RF-05.4** La temperatura corporal desciende pasivamente cada turno según: altitud, estado climático y si es turno nocturno.
- **RF-05.5** Si la temperatura corporal cae por debajo de 35°C, el jugador comienza a perder HP por hipotermia a razón proporcional a la diferencia.
- **RF-05.6** Si Stamina llega a 0, el jugador comienza a perder HP por agotamiento extremo.
- **RF-05.7** Willpower decrece pasivamente cada turno; la tasa aumenta con altitud, turnos transcurridos y `turns_above_8000`.
- **RF-05.8** Willpower por debajo de 20 impone una penalización de Stamina adicional del 15% (el jugador se arrastra mentalmente).
- **RF-05.9** La probabilidad de caída en **Avanzar (Agresivo)** es: `p_caida = 0.05 + max(0, (100 - stamina) / 100 × 0.3) × weather_mod × (1 - route_secured_bonus)`.
- **RF-05.10** El motor matemático debe ser una función pura sin efectos secundarios (sin I/O ni estado mutable externo).

### RF-06 — Sistema Climático

- **RF-06.1** El sistema modela cinco estados climáticos: `CLEAR`, `CLOUDY`, `WIND`, `STORM`, `WHITEOUT`.
- **RF-06.2** Las transiciones climáticas siguen una cadena de Markov. Cada estado tiene una distribución de probabilidad sobre el próximo estado, con mayor probabilidad de condiciones similares.
- **RF-06.3** El sistema proporciona al jugador un `weather_forecast` del siguiente turno, visible en la UI.
- **RF-06.4** El forecast es incorrecto ~25% de las veces (ruido gaussiano sobre la transición Markov).
- **RF-06.5** El sistema expone `forecast_reliability` (0.0–1.0) al frontend como indicador de calidad del pronóstico; este valor varía dinámicamente: disminuye en altitudes altas y en turnos nocturnos.
- **RF-06.6** Cada estado climático tiene un `weather_mod` que agrava el costo de acción: `CLEAR=1.0`, `CLOUDY=1.2`, `WIND=1.5`, `STORM=2.0`, `WHITEOUT=3.0`.
- **RF-06.7** `WHITEOUT` aumenta significativamente la probabilidad de eventos fatales y bloquea el avance si el jugador no tiene cuerda disponible.
- **RF-06.8** Las tormentas nocturnas durante **Acampar** tienen una probabilidad aumentada de activar el evento `TENT_COLLAPSE` (destrucción de campamento).

### RF-07 — Eventos Aleatorios

- **RF-07.1** El sistema implementa los siguientes tipos de eventos aleatorios:

| ID | Evento | Efecto principal |
|---|---|---|
| `DISTANT_AVALANCHE` | Avalancha lejana | Willpower −15, narra el sonido |
| `HALLUCINATION` | Alucinación por hipoxia | Willpower −20, información del turno distorsionada |
| `WIND_GUST` | Ráfaga violenta | Stamina −15, riesgo de caída si Stamina < 30 |
| `O2_REGULATOR_FAIL` | Fallo del regulador de O₂ | `oxygen_pct` cae a 0, gas_canisters −1 |
| `FROSTBITE` | Congelamiento de extremidades | HP −10/turno acumulativo, temperatura −2°C |
| `PULMONARY_EDEMA` | Edema pulmonar incipiente | HP −20, Stamina −30, requiere descender o morir |
| `TENT_COLLAPSE` | Colapso de carpa en tormenta | Stamina −25, temperatura −3°C |
| `PARTNER_VISION` | Visión de otro alpinista | Solo narrativo, sin efecto mecánico — atmósfera |
| `EQUIPMENT_DROP` | Pérdida de equipo | Pierde 1 sección de cuerda o 1 ración aleatoriamente |
| `SECOND_WIND` | Segundo aliento (positivo raro) | Stamina +20, Willpower +10 — narrativa inspiradora |

- **RF-07.2** La probabilidad base de eventos críticos (`PULMONARY_EDEMA`, `HALLUCINATION`) aumenta significativamente al entrar en la Zona de la Muerte (>8.000m) y con cada turno adicional en ella.
- **RF-07.3** Solo ocurre un máximo de un evento aleatorio por turno.
- **RF-07.4** Los eventos incluyen una descripción narrativa breve devuelta en la respuesta del servidor como campo `event.narrative`.
- **RF-07.5** Los eventos aplican penalizaciones directas a los atributos del jugador mediante el mismo sistema de deltas que las acciones normales.
- **RF-07.6** El evento `SECOND_WIND` solo puede ocurrir si el jugador lleva más de 10 turnos consecutivos sin recuperar Stamina (mecánica de recompensa por persistencia).

### RF-08 — Sistema de Psicología (Willpower)

- **RF-08.1** Willpower representa la resistencia mental del jugador y afecta mecánicas de juego más allá del narrativo.
- **RF-08.2** Willpower < 30 activa el estado `DOUBT`: las descripciones de acción en el `ActionPanel` cambian a texto dubitativo ("Intentar avanzar…", "¿Seguir?").
- **RF-08.3** Willpower < 15 activa el estado `DESPAIR`: el sistema agrega automáticamente el pensamiento de descender en el log narrativo y aumenta la probabilidad del evento `HALLUCINATION`.
- **RF-08.4** Willpower en 0 no provoca la muerte directamente, pero hace que la tasa de pérdida de HP por agotamiento se duplique.
- **RF-08.5** Las acciones **Comer** y **Usar Oxígeno** recuperan Willpower levemente. **Acampar** recupera Willpower si el clima es favorable.
- **RF-08.6** Llegar al Hombro (>8.000m) por primera vez otorga un bonus fijo de +25 Willpower como recompensa narrativa.

### RF-09 — Condiciones de Victoria y Derrota

- **RF-09.1** El jugador gana si alcanza o supera 8.611m con HP > 0.
- **RF-09.2** El jugador pierde si su HP llega a 0.
- **RF-09.3** El sistema diferencia la causa de muerte: `DEAD_EXHAUSTION`, `DEAD_COLD`, `DEAD_FALL`, `DEAD_STORM`, `DEAD_EDEMA`.
- **RF-09.4** Al ganar, el sistema devuelve un resumen completo: turnos totales, altitud máxima, recursos restantes, causa de los peores momentos.
- **RF-09.5** Al perder, el sistema devuelve la causa de muerte, la altitud máxima alcanzada y el turno de muerte.
- **RF-09.6** Tras el fin de la partida, el jugador puede iniciar una nueva sesión desde la pantalla de resultado.
- **RF-09.7** El sistema genera y devuelve una **epitafio narrativo** único en cada derrota, generado por `NarrativeService` con el contexto de la sesión.

### RF-10 — Interfaz de Usuario

- **RF-10.1** La interfaz muestra en todo momento los cuatro atributos vitales (HP, Stamina, Temperatura, Willpower) como barras de progreso con color semántico.
- **RF-10.2** La altitud actual se visualiza como una barra vertical que representa el progreso desde 5.200m hasta 8.611m, con la Zona de la Muerte marcada en rojo desde 8.000m.
- **RF-10.3** Los recursos consumibles (comida, gas, cuerda, oxígeno) se muestran como contadores siempre visibles.
- **RF-10.4** El clima actual y el pronóstico del siguiente turno se muestran simultáneamente con iconografía diferenciada e indicador de fiabilidad del forecast.
- **RF-10.5** Los deltas de atributos se animan con valores positivos en verde y negativos en rojo, con transición de 600ms.
- **RF-10.6** El log narrativo muestra los últimos eventos con scroll, preservando el historial completo de la sesión.
- **RF-10.7** Las acciones disponibles se muestran como botones con descripción del costo estimado visible antes de confirmar. Las acciones irreversibles o costosas requieren confirmación en modal.
- **RF-10.8** La interfaz bloquea la entrada del jugador mientras el servidor procesa el turno.
- **RF-10.9** El diseño es responsive y funciona en pantallas de al menos 1024px de ancho.
- **RF-10.10** La Zona de la Muerte (>8.000m) se refleja visualmente: cambio de paleta a tonos más fríos y saturados, indicador de advertencia pulsante, overlay de partículas de nieve.
- **RF-10.11** Los estados `DOUBT` y `DESPAIR` de Willpower modifican visualmente el `ActionPanel`: tipografía más tenue, animaciones temblorosas, texto alternativo en botones.
- **RF-10.12** El ciclo día/noche se refleja en la UI: fondos más oscuros durante turnos nocturnos (12–23), indicador de hora de expedición visible.

### RF-11 — API REST

- **RF-11.1** `POST /game/new` — crea sesión, devuelve estado inicial con narrativa de introducción.
- **RF-11.2** `POST /game/turn` — recibe `session_id` y `action`, procesa el turno, devuelve `TurnResponse` completo con deltas.
- **RF-11.3** `GET /game/state/{session_id}` — devuelve estado actual sin modificarlo.
- **RF-11.4** `DELETE /game/session/{session_id}` — elimina la sesión del almacenamiento.
- **RF-11.5** Todos los endpoints devuelven errores descriptivos con código HTTP apropiado (404 sesión no encontrada, 409 sesión no activa, 422 acción inválida).
- **RF-11.6** El backend configura CORS para permitir solicitudes desde el origen del frontend.
- **RF-11.7** Los endpoints respetan el contrato de schemas definidos en `schemas/game.py`. Cualquier cambio en schemas es considerado breaking change.

### RF-12 — Narrativa con IA

- **RF-12.1** El `NarrativeService` genera texto narrativo por turno consumiendo el `TurnResult` completo (deltas, evento, clima, altitud, estado psicológico).
- **RF-12.2** La generación narrativa es **no bloqueante**: si falla o supera 1.5s, el sistema devuelve texto de fallback local sin interrumpir el turno.
- **RF-12.3** El sistema mantiene una ventana de contexto narrativo de los últimos 5 turnos para mantener coherencia en la voz del narrador.
- **RF-12.4** La voz narrativa cambia según el estado de Willpower: objetiva y precisa en niveles altos, fragmentada y desesperada en niveles bajos.
- **RF-12.5** El `NarrativeService` es configurable: puede usar generación local (templates) o Anthropic API según la variable de entorno `NARRATIVE_MODE`.
- **RF-12.6** La narrativa del epitafio final (derrota) incluye la causa de muerte, la altitud máxima, el evento que desencadenó el fin y una frase final en latín.

---

## Requerimientos No Funcionales

| ID | Requerimiento |
|---|---|
| **RNF-01** | El servidor responde cada turno en < 200ms en condiciones normales (excluyendo la llamada a Narrative API). |
| **RNF-02** | El motor de juego puede ser migrado de memoria a Redis sin cambios en `game_engine.py` ni en los routers. |
| **RNF-03** | La UI no muestra datos desactualizados: cada render refleja el estado devuelto por el último turno procesado. |
| **RNF-04** | El código del motor matemático (`game_engine.py`) tiene cobertura de tests ≥ 80% antes de producción. |
| **RNF-05** | La generación narrativa tiene un timeout de 1.5s con fallback a templates locales para garantizar RNF-01. |
| **RNF-06** | El `SessionRepository` abstrae el almacenamiento mediante un Protocol; la implementación es intercambiable sin modificar servicios. |

---

## Decisiones de Diseño

**Sesiones en memoria para MVP.** Un `dict[session_id → GameState]` valida la mecánica sin dependencias externas. El `AbstractSessionRepository` garantiza que la migración a Redis sea un cambio de implementación, no de arquitectura.

**Los deltas van en la respuesta.** El backend devuelve `stamina_delta`, `hp_delta`, etc. El frontend los usa para animar cambios sin recalcular nada por su cuenta. Single source of truth.

**El pronóstico miente.** El backend mantiene `weather` (real) y `weather_forecast` (lo que ve el jugador). El frontend solo muestra el forecast. La tensión nace de esa información incompleta. `forecast_reliability` añade una capa de meta-incertidumbre.

**Willpower como capa psicológica mecánica.** No es solo flavor: afecta la UI, modifica las tasas de pérdida de HP y cambia el texto de los botones de acción. El juego se degrada visualmente conforme el jugador se deteriora mentalmente.

**Sin auth en MVP.** El `session_id` es el único identificador. Auth se agrega cuando haya tabla de rankings o perfiles.

**La narrativa es desacoplada y opcional.** El motor matemático no sabe nada de la IA narrativa. El `NarrativeService` es un consumidor del `TurnResult`, no un participante. Esto permite desactivarlo en tests y en entornos sin API key sin romper ninguna lógica de juego.

**Ciclo día/noche sin calendario.** El número de turno modulo 24 determina si es día o noche. No hay gestión de fechas reales. El beneficio narrativo y mecánico es alto; el costo de implementación es mínimo.