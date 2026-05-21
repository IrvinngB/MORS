<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeTab = ref<'basics' | 'actions' | 'environment' | 'tips'>('basics')

function onBack() {
  router.push('/')
}
</script>

<template>
  <div class="relative min-h-screen bg-[#03030a] flex flex-col items-center overflow-x-hidden overflow-y-auto px-4 py-8">
    <!-- Background gradients & aesthetics -->
    <div class="absolute inset-0 bg-gradient-to-b from-[#020205] via-[#08081a] to-peak/15 pointer-events-none" />
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_30%,rgba(0,0,0,0.8)_100%)] pointer-events-none z-20" />

    <!-- Content Container -->
    <div class="relative z-30 w-full max-w-4xl animate-fade-in flex flex-col min-h-full">
      
      <!-- Header -->
      <div class="text-center mb-6">
        <h1 class="text-3xl md:text-4xl font-black tracking-[0.2em] text-snow uppercase bg-clip-text bg-gradient-to-r from-snow via-ice to-glacier">
          Manual de Supervivencia
        </h1>
        <p class="text-ice/40 text-xs tracking-widest mt-1 uppercase">
          K2 — 8611m • Guía Técnica para Expedicionarios
        </p>
      </div>

      <!-- Interactive Navigation Tabs -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-2 mb-6">
        <!-- Tab: Básicos -->
        <button 
          @click="activeTab = 'basics'"
          :class="[
            'flex items-center justify-center gap-2 p-3 rounded-lg border transition-all duration-300 font-bold text-xs tracking-wider uppercase cursor-pointer',
            activeTab === 'basics' 
              ? 'border-glacier/40 bg-glacier/10 text-glacier shadow-[0_0_15px_rgba(116,185,255,0.07)]' 
              : 'border-white/5 bg-white/2 hover:bg-white/5 text-ice/50 hover:text-ice'
          ]"
        >
          <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M8 3l4 8 5-5 7 14H0z"/>
          </svg>
          Básicos
        </button>

        <!-- Tab: Acciones -->
        <button 
          @click="activeTab = 'actions'"
          :class="[
            'flex items-center justify-center gap-2 p-3 rounded-lg border transition-all duration-300 font-bold text-xs tracking-wider uppercase cursor-pointer',
            activeTab === 'actions' 
              ? 'border-warning/40 bg-warning/10 text-warning shadow-[0_0_15px_rgba(243,156,18,0.07)]' 
              : 'border-white/5 bg-white/2 hover:bg-white/5 text-ice/50 hover:text-ice'
          ]"
        >
          <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
          </svg>
          Acciones
        </button>

        <!-- Tab: Clima -->
        <button 
          @click="activeTab = 'environment'"
          :class="[
            'flex items-center justify-center gap-2 p-3 rounded-lg border transition-all duration-300 font-bold text-xs tracking-wider uppercase cursor-pointer',
            activeTab === 'environment' 
              ? 'border-mors/40 bg-mors/10 text-mors shadow-[0_0_15px_rgba(155,89,182,0.07)]' 
              : 'border-white/5 bg-white/2 hover:bg-white/5 text-ice/50 hover:text-ice'
          ]"
        >
          <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>
          </svg>
          Entorno
        </button>

        <!-- Tab: Tips -->
        <button 
          @click="activeTab = 'tips'"
          :class="[
            'flex items-center justify-center gap-2 p-3 rounded-lg border transition-all duration-300 font-bold text-xs tracking-wider uppercase cursor-pointer',
            activeTab === 'tips' 
              ? 'border-success/40 bg-success/10 text-success shadow-[0_0_15px_rgba(46,204,113,0.07)]' 
              : 'border-white/5 bg-white/2 hover:bg-white/5 text-ice/50 hover:text-ice'
          ]"
        >
          <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/>
          </svg>
          Consejos
        </button>
      </div>

      <!-- Tab Content Area -->
      <div class="flex-1 min-h-[400px]">

        <!-- TAB 1: BASICS -->
        <div v-if="activeTab === 'basics'" class="space-y-4 animate-fade-in">
          <!-- Objetivo -->
          <div class="glass p-5 rounded-xl border border-white/5 relative overflow-hidden">
            <div class="absolute top-0 right-0 w-24 h-24 bg-glacier/5 blur-2xl rounded-full" />
            <h2 class="text-sm font-bold text-snow uppercase tracking-widest flex items-center gap-2 mb-2">
              <span class="w-1.5 h-1.5 bg-glacier rounded-full"></span>
              Misión de la Expedición
            </h2>
            <p class="text-ice/70 text-xs leading-relaxed">
              El objetivo principal es llevar a tu alpinista a la cima del <span class="text-snow font-bold">K2 (8.611m)</span> de forma segura y regresar vivo. Comenzás la aventura en el Campamento Base a <span class="text-glacier font-bold">5.200m</span>. Cada acción consume recursos físicos y tiempo. Recordá: la cima es opcional, el descenso y la supervivencia son obligatorios.
            </p>
          </div>

          <!-- Stats Clave -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Stats Físicos -->
            <div class="glass p-5 rounded-xl border border-white/5">
              <h3 class="text-xs font-bold text-snow uppercase tracking-widest mb-3 flex items-center gap-2">
                <span class="w-1 h-3 bg-danger rounded-full"></span>
                Indicadores Físicos
              </h3>
              <div class="space-y-3">
                <div class="flex gap-3">
                  <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-danger/10 border border-danger/20 text-danger uppercase shrink-0 h-fit">HP</span>
                  <p class="text-ice/70 text-[11px] leading-relaxed">
                    <span class="text-snow font-semibold">Salud vital.</span> Si desciende a 0, sobreviene la muerte inmediata. No se recupera de forma pasiva, requiere cuidados especiales o habilidades.
                  </p>
                </div>
                <div class="flex gap-3">
                  <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-warning/10 border border-warning/20 text-warning uppercase shrink-0 h-fit">STA</span>
                  <p class="text-ice/70 text-[11px] leading-relaxed">
                    <span class="text-snow font-semibold">Stamina.</span> La energía requerida para moverte. Si llega a 0, perdés salud (HP) progresivamente en cada turno de esfuerzo.
                  </p>
                </div>
                <div class="flex gap-3">
                  <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-glacier/10 border border-glacier/20 text-glacier uppercase shrink-0 h-fit">TEMP</span>
                  <p class="text-ice/70 text-[11px] leading-relaxed">
                    <span class="text-snow font-semibold">Temperatura Corporal.</span> Rango saludable: 35.0°C - 38.0°C. Si baja de 35.0°C sufrís hipotermia y perdés HP cada turno.
                  </p>
                </div>
              </div>
            </div>

            <!-- Stats Mentales y Zona de Muerte -->
            <div class="glass p-5 rounded-xl border border-white/5 flex flex-col justify-between">
              <div>
                <h3 class="text-xs font-bold text-snow uppercase tracking-widest mb-3 flex items-center gap-2">
                  <span class="w-1 h-3 bg-mors rounded-full"></span>
                  Mente y Altitud
                </h3>
                <div class="space-y-3">
                  <div class="flex gap-3">
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-mors/10 border border-mors/20 text-mors uppercase shrink-0 h-fit">WP</span>
                    <p class="text-ice/70 text-[11px] leading-relaxed">
                      <span class="text-snow font-semibold">Fuerza de Voluntad.</span> Si cae por debajo de 30, tu rendimiento físico disminuye incrementando gradualmente el costo de stamina.
                    </p>
                  </div>
                </div>
              </div>

              <!-- Zona de la Muerte -->
              <div class="mt-4 p-3 rounded bg-danger/5 border border-danger/10">
                <h4 class="text-[11px] font-bold text-danger uppercase tracking-widest mb-1 flex items-center gap-1.5">
                  Zona de la Muerte (≥8000m)
                </h4>
                <p class="text-ice/60 text-[10px] leading-relaxed">
                  A esta altitud el cuerpo se degrada. El oxígeno ambiental cae al mínimo, la voluntad se deteriora y el frío es letal. Tu primer cruce por la frontera de los 8000m te otorga un shock de adrenalina de <span class="text-success font-bold">+15 WP</span>.
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- TAB 2: ACTIONS -->
        <div v-if="activeTab === 'actions'" class="space-y-4 animate-fade-in">
          <!-- Listado de Acciones -->
          <div class="glass p-5 rounded-xl border border-white/5">
            <h2 class="text-sm font-bold text-snow uppercase tracking-widest mb-4 flex items-center gap-2">
              <span class="w-1.5 h-1.5 bg-warning rounded-full"></span>
              Acciones y Costos de Recursos
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <!-- Acción 1 -->
              <div class="p-3 bg-white/2 rounded-lg border border-white/5 flex flex-col justify-between">
                <div>
                  <div class="flex justify-between items-center mb-1">
                    <span class="text-xs font-bold text-snow">Avanzar</span>
                    <span class="text-[9px] px-2 py-0.5 rounded bg-glacier/10 text-glacier border border-glacier/10 font-bold uppercase">+150m</span>
                  </div>
                  <p class="text-ice/60 text-[10px] leading-relaxed">Ascenso regular y estable. Costo base normal.</p>
                </div>
              </div>

              <!-- Acción 2 -->
              <div class="p-3 bg-white/2 rounded-lg border border-white/5 flex flex-col justify-between">
                <div>
                  <div class="flex justify-between items-center mb-1">
                    <span class="text-xs font-bold text-snow">Avanzar Agresivo</span>
                    <span class="text-[9px] px-2 py-0.5 rounded bg-warning/10 text-warning border border-warning/10 font-bold uppercase">+280m • Riesgo Caída</span>
                  </div>
                  <p class="text-ice/60 text-[10px] leading-relaxed">Avanza el doble pero con riesgo de sufrir una caída peligrosa.</p>
                </div>
              </div>

              <!-- Acción 3 -->
              <div class="p-3 bg-white/2 rounded-lg border border-white/5 flex flex-col justify-between">
                <div>
                  <div class="flex justify-between items-center mb-1">
                    <span class="text-xs font-bold text-snow">Asegurar Ruta</span>
                    <span class="text-[9px] px-2 py-0.5 rounded bg-danger/10 text-danger border border-danger/10 font-bold uppercase">Usa 1 Cuerda</span>
                  </div>
                  <p class="text-ice/60 text-[10px] leading-relaxed">Instala cuerdas fijas para proteger los siguientes 3 turnos contra vientos y whiteouts.</p>
                </div>
              </div>

              <!-- Acción 4 -->
              <div class="p-3 bg-white/2 rounded-lg border border-white/5 flex flex-col justify-between">
                <div>
                  <div class="flex justify-between items-center mb-1">
                    <span class="text-xs font-bold text-snow">Acampar</span>
                    <span class="text-[9px] px-2 py-0.5 rounded bg-success/10 text-success border border-success/10 font-bold uppercase">1 Comida + 1 Gas</span>
                  </div>
                  <p class="text-ice/60 text-[10px] leading-relaxed">Establece refugio para recuperar stamina y calentarte.</p>
                </div>
              </div>

              <!-- Acción 5 -->
              <div class="p-3 bg-white/2 rounded-lg border border-white/5 flex flex-col justify-between">
                <div>
                  <div class="flex justify-between items-center mb-1">
                    <span class="text-xs font-bold text-snow">Usar Oxígeno</span>
                    <span class="text-[9px] px-2 py-0.5 rounded bg-info/10 text-glacier border border-glacier/25 font-bold uppercase">1 Tanque O₂</span>
                  </div>
                  <p class="text-ice/60 text-[10px] leading-relaxed">Abre un tanque para recuperar +30% O₂ y subir +10 la voluntad.</p>
                </div>
              </div>

              <!-- Acción 6 -->
              <div class="p-3 bg-white/2 rounded-lg border border-white/5 flex flex-col justify-between">
                <div>
                  <div class="flex justify-between items-center mb-1">
                    <span class="text-xs font-bold text-snow">Comer / Descender</span>
                    <span class="text-[9px] px-2 py-0.5 rounded bg-white/5 text-ice/80 border border-white/10 font-bold uppercase">Gestión básica</span>
                  </div>
                  <p class="text-ice/60 text-[10px] leading-relaxed">Comer gasta 1 ración (+stamina). Descender retrocede 200m para resguardarse.</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Fórmula de Stamina -->
          <div class="glass p-5 rounded-xl border border-white/5">
            <h2 class="text-sm font-bold text-snow uppercase tracking-widest mb-3 flex items-center gap-2">
              <span class="w-1.5 h-1.5 bg-glacier rounded-full"></span>
              Ecuación de Esfuerzo (Stamina)
            </h2>
            <div class="bg-black/40 rounded-lg p-4 font-mono text-[11px] text-ice/80 space-y-2 border border-white/5">
              <div class="text-glacier font-bold mb-2">costo_turno = Base (12.0) × altitud_factor × clima × oxígeno × voluntad × rol</div>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-1 text-ice/60 border-t border-white/5 pt-2 mt-2">
                <p><span class="text-snow">Altitud:</span> 1 + (altitud / 8000)²</p>
                <p><span class="text-snow">Voluntad:</span> &lt;30 = 1.05 | &lt;20 = 1.15 | &lt;10 = 1.25</p>
                <p><span class="text-snow">Noche:</span> Turnos 12–23 aplican multiplicador 1.3×</p>
                <p><span class="text-snow">Clima:</span> CLEAR=1.0 | STORM=2.0 | WHITEOUT=3.0</p>
              </div>
            </div>
          </div>
        </div>

        <!-- TAB 3: ENVIRONMENT -->
        <div v-if="activeTab === 'environment'" class="space-y-4 animate-fade-in">
          <!-- Clima Markov -->
          <div class="glass p-5 rounded-xl border border-white/5">
            <h2 class="text-sm font-bold text-snow uppercase tracking-widest mb-3 flex items-center gap-2">
              <span class="w-1.5 h-1.5 bg-mors rounded-full"></span>
              Modificadores Climáticos
            </h2>
            <div class="grid grid-cols-2 md:grid-cols-5 gap-2">
              <div class="p-3 bg-white/2 rounded-lg border border-white/5 text-center">
                <div class="text-xs font-bold text-snow">CLEAR</div>
                <div class="text-[10px] text-success font-bold mt-1">×1.0 Costo</div>
              </div>
              <div class="p-3 bg-white/2 rounded-lg border border-white/5 text-center">
                <div class="text-xs font-bold text-ice/80">CLOUDY</div>
                <div class="text-[10px] text-ice/60 font-bold mt-1">×1.2 Costo</div>
              </div>
              <div class="p-3 bg-white/2 rounded-lg border border-white/5 text-center">
                <div class="text-xs font-bold text-warning/80">WIND</div>
                <div class="text-[10px] text-warning/80 font-bold mt-1">×1.5 Costo</div>
              </div>
              <div class="p-3 bg-white/2 rounded-lg border border-white/5 text-center">
                <div class="text-xs font-bold text-danger/80">STORM</div>
                <div class="text-[10px] text-danger/80 font-bold mt-1">×2.0 Costo</div>
              </div>
              <div class="p-3 bg-white/2 rounded-lg border border-white/5 text-center col-span-2 md:col-span-1">
                <div class="text-xs font-bold text-white">WHITEOUT</div>
                <div class="text-[10px] text-white font-bold mt-1">×3.0 Costo</div>
              </div>
            </div>
            <p class="text-ice/50 text-[10px] mt-3 leading-relaxed">
              <span class="text-snow font-bold">El pronóstico climático tiene un ~25% de error.</span> La confiabilidad se degrada con la altura y durante la noche. El rol Investigador compensa esto con un bonus pasivo permanente.
            </p>
          </div>

          <!-- Ciclo de Turnos y Eventos -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Noche -->
            <div class="glass p-5 rounded-xl border border-white/5">
              <h3 class="text-xs font-bold text-snow uppercase tracking-widest mb-2 flex items-center gap-2">
                Ciclo Día/Noche
              </h3>
              <p class="text-ice/70 text-[11px] leading-relaxed">
                El día dura del turno 0 al 11; la noche inicia del turno 12 al 23. Moverse de noche añade un <span class="text-snow font-bold">30% de penalización</span> a la stamina, y acampar de noche rinde un <span class="text-snow font-bold">15% menos</span>. Planificá tus campamentos antes del atardecer.
              </p>
            </div>

            <!-- Eventos -->
            <div class="glass p-5 rounded-xl border border-white/5">
              <h3 class="text-xs font-bold text-snow uppercase tracking-widest mb-2 flex items-center gap-2">
                Eventos Aleatorios
              </h3>
              <p class="text-ice/70 text-[11px] leading-relaxed">
                Se calcula un evento por turno como máximo. El clima extremo y la altitud disparan la probabilidad de avalanchas, tormentas repentinas o problemas de salud.
              </p>
              <div class="mt-2 text-[10px] text-glacier">
                <span class="font-bold">Second Wind:</span> Si pasás 10 turnos seguidos sin recuperar stamina, recibirás un empujón de adrenalina gratis.
              </div>
            </div>
          </div>
        </div>

        <!-- TAB 4: TIPS -->
        <div v-if="activeTab === 'tips'" class="space-y-4 animate-fade-in">
          <!-- Pro Tips -->
          <div class="glass p-5 rounded-xl border border-white/5">
            <h2 class="text-sm font-bold text-snow uppercase tracking-widest mb-4 flex items-center gap-2">
              <span class="w-1.5 h-1.5 bg-success rounded-full"></span>
              Consejos de Alpinistas Experimentados
            </h2>
            <div class="space-y-3">
              <div class="p-3 bg-white/2 rounded-lg border border-white/5 flex gap-3 items-start">
                <svg class="w-4 h-4 text-success shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M8 3l4 8 5-5 7 14H0z"/>
                </svg>
                <div>
                  <h4 class="text-xs font-bold text-snow">La Cuerda es tu salvavidas</h4>
                  <p class="text-ice/60 text-[10px] leading-relaxed mt-0.5">En clima de Whiteout (viento blanco) no podés avanzar si no tenés la ruta asegurada. Fijá cuerdas antes de que la tormenta te atrape.</p>
                </div>
              </div>
              <div class="p-3 bg-white/2 rounded-lg border border-white/5 flex gap-3 items-start">
                <svg class="w-4 h-4 text-success shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"/><path d="m12 8-4 4h8z"/>
                </svg>
                <div>
                  <h4 class="text-xs font-bold text-snow">Gestioná el Oxígeno en la Zona de la Muerte</h4>
                  <p class="text-ice/60 text-[10px] leading-relaxed mt-0.5">Por encima de los 8000m tu O₂ cae 5% en cada turno. Mantené tu válvula abierta únicamente cuando sea crítico para reducir el gasto de stamina, o consumí un tanque.</p>
                </div>
              </div>
              <div class="p-3 bg-white/2 rounded-lg border border-white/5 flex gap-3 items-start">
                <svg class="w-4 h-4 text-success shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>
                </svg>
                <div>
                  <h4 class="text-xs font-bold text-snow">La temperatura mata en silencio</h4>
                  <p class="text-ice/60 text-[10px] leading-relaxed mt-0.5">Si tu temperatura desciende de los 35°C, tu vida drenará velozmente por hipotermia. Asegurá siempre tener comida y gas para acampar a salvo de noche.</p>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Footer navigation -->
      <div class="mt-6 text-center">
        <button
          class="text-ice/40 hover:text-snow transition-all duration-200 text-xs tracking-widest uppercase cursor-pointer py-2 px-4 hover:bg-white/3 rounded-lg border border-transparent hover:border-white/5"
          @click="onBack"
        >
          ← Volver al Menú Principal
        </button>
      </div>

    </div>
  </div>
</template>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
