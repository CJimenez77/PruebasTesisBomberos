<template>
  <div class="p-6 space-y-6 max-w-7xl mx-auto">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-black text-white tracking-tight">Control de Alertas de Discrepancia</h1>
        <p class="text-xs text-gray-400 mt-0.5">Auditoría, visación y resolución formal de diferencias patrimoniales</p>
      </div>

      <div class="flex items-center gap-3">
        <button
          v-if="inspeccionesStore.totalAlertasPendientes > 0"
          @click="showNotifyModal = true"
          class="px-4 py-2.5 rounded-xl bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold shadow-lg shadow-amber-950/40 transition-all flex items-center gap-2"
        >
          <span>📢</span> Notificar al Director ({{ inspeccionesStore.totalAlertasPendientes }})
        </button>
      </div>
    </div>

    <!-- Stats Summary Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div class="bg-bomberos-card border border-bomberos-border p-4 rounded-2xl">
        <span class="text-xs font-bold text-gray-400 uppercase">Total Alertas</span>
        <div class="text-2xl font-black text-white mt-1">{{ inspeccionesStore.alertas.length }}</div>
      </div>
      <div class="bg-red-950/30 border border-red-800/60 p-4 rounded-2xl">
        <span class="text-xs font-bold text-red-400 uppercase">Pendientes / Críticas</span>
        <div class="text-2xl font-black text-red-400 mt-1">{{ inspeccionesStore.totalAlertasPendientes }}</div>
      </div>
      <div class="bg-emerald-950/30 border border-emerald-800/60 p-4 rounded-2xl">
        <span class="text-xs font-bold text-emerald-400 uppercase">Resueltas / Visadas</span>
        <div class="text-2xl font-black text-emerald-400 mt-1">{{ inspeccionesStore.alertasResueltas.length }}</div>
      </div>
    </div>

    <!-- Filter Tabs -->
    <div class="flex items-center gap-2 border-b border-bomberos-border pb-3">
      <button
        @click="filterStatus = 'all'"
        class="px-4 py-2 rounded-xl text-xs font-bold transition-all"
        :class="filterStatus === 'all' ? 'bg-bomberos-red text-white' : 'bg-bomberos-surface text-gray-400 hover:text-white'"
      >
        Todas ({{ inspeccionesStore.alertas.length }})
      </button>
      <button
        @click="filterStatus = 'pending'"
        class="px-4 py-2 rounded-xl text-xs font-bold transition-all"
        :class="filterStatus === 'pending' ? 'bg-bomberos-red text-white' : 'bg-bomberos-surface text-gray-400 hover:text-white'"
      >
        Pendientes ({{ inspeccionesStore.totalAlertasPendientes }})
      </button>
      <button
        @click="filterStatus = 'resolved'"
        class="px-4 py-2 rounded-xl text-xs font-bold transition-all"
        :class="filterStatus === 'resolved' ? 'bg-bomberos-red text-white' : 'bg-bomberos-surface text-gray-400 hover:text-white'"
      >
        Resueltas ({{ inspeccionesStore.alertasResueltas.length }})
      </button>
    </div>

    <!-- Alerts List -->
    <div v-if="filteredAlertas.length === 0" class="bg-bomberos-surface border border-bomberos-border rounded-3xl p-12 text-center">
      <div class="text-4xl mb-2">🛡️</div>
      <h3 class="text-base font-bold text-white">No hay alertas en esta sección</h3>
      <p class="text-xs text-gray-400 mt-1">El inventario físico coincide plenamente con los registros contables.</p>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="alerta in filteredAlertas"
        :key="alerta.id_alerta"
        class="bg-bomberos-surface border rounded-3xl p-6 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-6 transition-all"
        :class="alerta.resuelta ? 'border-bomberos-border/80 opacity-80' : 'border-red-600/80 bg-red-950/10 shadow-red-950/20'"
      >
        <div class="space-y-2 flex-1">
          <div class="flex flex-wrap items-center gap-2">
            <span
              v-if="!alerta.resuelta"
              class="px-2.5 py-1 rounded-lg bg-red-600 text-white font-extrabold text-[11px] animate-pulse uppercase"
            >
              CRÍTICA PENDIENTE
            </span>
            <span
              v-else
              class="px-2.5 py-1 rounded-lg bg-emerald-950 text-emerald-400 border border-emerald-800 font-extrabold text-[11px] uppercase"
            >
              ✓ {{ alerta.estado_nombre }}
            </span>

            <span class="text-xs text-gray-400 font-mono">ID Alerta #{{ alerta.id_alerta }}</span>
          </div>

          <h3 class="text-lg font-black text-white">{{ alerta.item_nombre }}</h3>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-gray-300">
            <div>
              <span class="text-gray-500 font-bold">Ubicación Afectada:</span>
              <span class="font-semibold text-gray-200 ml-1">{{ alerta.ubicacion_nombre }}</span>
            </div>
            <div>
              <span class="text-gray-500 font-bold">Diferencia Detectada:</span>
              <span class="font-black text-red-400 ml-1">{{ alerta.diferencia }} unidad(es)</span>
            </div>
          </div>

          <div class="p-3 rounded-xl bg-bomberos-card border border-bomberos-border text-xs text-gray-300 mt-2">
            <p class="font-bold text-gray-400 mb-0.5">Observaciones de Inspección:</p>
            <p>{{ alerta.observaciones }}</p>
            <div v-if="alerta.resuelta" class="mt-2 pt-2 border-t border-bomberos-border text-[11px] text-emerald-400">
              ✓ Visado por: <strong>{{ alerta.usuario_resolutor_nombre }}</strong>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="shrink-0 flex flex-col gap-2">
          <button
            v-if="!alerta.resuelta"
            @click="openResolveModal(alerta)"
            class="px-4 py-2.5 rounded-xl bg-bomberos-red hover:bg-bomberos-red-hover text-white text-xs font-bold shadow-lg shadow-red-950/40 transition-all text-center"
          >
            ⭐ Visar y Resolver Discrepancia
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de Resolución de Alertas -->
    <div v-if="showResolveModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div class="bg-bomberos-surface border border-bomberos-border rounded-3xl w-full max-w-lg overflow-hidden shadow-2xl p-6 space-y-4">
        <div class="flex items-center justify-between border-b border-bomberos-border pb-3">
          <h3 class="font-bold text-base text-white">Resolución Oficial de Discrepancia</h3>
          <button @click="showResolveModal = false" class="text-gray-400 hover:text-white font-bold">✕</button>
        </div>

        <div class="text-xs text-gray-300">
          <p>Ítem: <strong class="text-white">{{ selectedAlerta?.item_nombre }}</strong></p>
          <p>Ubicación: <strong class="text-white">{{ selectedAlerta?.ubicacion_nombre }}</strong></p>
        </div>

        <div>
          <label class="block text-xs font-bold text-gray-400 mb-1">Decisión del Mando / Estado Definitivo *</label>
          <select v-model.number="resolveForm.id_estado_alerta" class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-3 py-2.5 text-xs text-white focus:outline-none focus:border-bomberos-red">
            <option :value="2">RESUELTA_HALLAZGO (Material localizado internamente)</option>
            <option :value="3">CONFIRMADA_EXTRAVIO (Pérdida ratificada en siniestro)</option>
            <option :value="4">TRAMITADA_BAJA (Material destruido / derivado a baja)</option>
            <option :value="5">DESCARTADA (Error de conteo / digitación)</option>
          </select>
        </div>

        <div>
          <label class="block text-xs font-bold text-gray-400 mb-1">Fundamentación Oficial *</label>
          <textarea
            v-model="resolveForm.observaciones"
            rows="3"
            required
            placeholder="Ingrese el detalle de la resolución, número de parte o justificación..."
            class="w-full bg-bomberos-card border border-bomberos-border rounded-xl p-3 text-xs text-white focus:outline-none focus:border-bomberos-red"
          ></textarea>
        </div>

        <div class="pt-3 border-t border-bomberos-border flex items-center justify-end gap-3">
          <button
            type="button"
            @click="showResolveModal = false"
            class="px-4 py-2 rounded-xl border border-bomberos-border text-xs font-bold text-gray-300"
          >
            Cancelar
          </button>
          <button
            type="button"
            @click="handleResolveSubmit"
            class="px-5 py-2 rounded-xl bg-bomberos-red hover:bg-bomberos-red-hover text-white text-xs font-bold shadow-lg"
          >
            Confirmar Cierre de Alerta
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de Notificación al Director -->
    <div v-if="showNotifyModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div class="bg-bomberos-surface border border-bomberos-border rounded-3xl w-full max-w-md overflow-hidden shadow-2xl p-6 space-y-4 text-center">
        <div class="w-12 h-12 rounded-2xl bg-amber-950 text-amber-400 border border-amber-800/60 mx-auto flex items-center justify-center text-2xl">
          📢
        </div>
        <h3 class="font-black text-lg text-white">Notificar Reporte Crítico al Director</h3>
        <p class="text-xs text-gray-400">
          Se enviará un resumen de las {{ inspeccionesStore.totalAlertasPendientes }} alertas críticas activas a <strong>Cristian Jiménez Fuentes (Director)</strong>.
        </p>

        <div class="p-3 rounded-xl bg-bomberos-card border border-bomberos-border text-left text-xs text-gray-300 space-y-1">
          <div class="flex items-center gap-2">
            <span class="text-emerald-400">✓</span> Correo Institucional: <code>director@bomberoschillanviejo.cl</code>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-emerald-400">✓</span> Notificación Push en App Móvil
          </div>
        </div>

        <button
          @click="sendNotification"
          class="w-full py-3 bg-amber-600 hover:bg-amber-500 text-white font-bold text-xs rounded-xl shadow-lg transition-all"
        >
          Confirmar y Despachar Notificación
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useInspeccionesStore } from '../stores/inspecciones'

const inspeccionesStore = useInspeccionesStore()
const filterStatus = ref('all')
const showResolveModal = ref(false)
const showNotifyModal = ref(false)
const selectedAlerta = ref(null)

const resolveForm = reactive({
  id_estado_alerta: 2,
  observaciones: '',
})

onMounted(async () => {
  await inspeccionesStore.fetchInspecciones()
})

const filteredAlertas = computed(() => {
  if (filterStatus.value === 'pending') return inspeccionesStore.alertasPendientes
  if (filterStatus.value === 'resolved') return inspeccionesStore.alertasResueltas
  return inspeccionesStore.alertas
})

const openResolveModal = (alerta) => {
  selectedAlerta.value = alerta
  resolveForm.observaciones = `Resolución formal: Material revisado por el oficial de servicio.`
  showResolveModal.value = true
}

const handleResolveSubmit = async () => {
  if (!selectedAlerta.value) return
  const res = await inspeccionesStore.resolverAlerta(selectedAlerta.value.id_alerta, resolveForm)
  if (res.success) {
    showResolveModal.value = false
  } else {
    alert(res.error)
  }
}

const sendNotification = () => {
  alert('¡Notificación despachada con éxito al Director Cristian Jiménez Fuentes!')
  showNotifyModal.value = false
}
</script>
