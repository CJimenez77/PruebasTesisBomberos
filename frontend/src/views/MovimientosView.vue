<template>
  <div class="p-6 space-y-6 max-w-7xl mx-auto">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-black text-white tracking-tight">Bitácora de Trazabilidad & Movimientos</h1>
        <p class="text-xs text-gray-400 mt-0.5">Ledger inmutable append-only con auditoría de traslados, compras y bajas</p>
      </div>

      <div class="flex items-center gap-3">
        <button
          @click="showModal = true"
          class="px-4 py-2.5 rounded-xl bg-bomberos-red hover:bg-bomberos-red-hover text-white text-xs font-bold shadow-lg shadow-red-950/40 transition-all flex items-center gap-2"
        >
          <span>🔄</span> Registrar Traslado / Movimiento
        </button>
      </div>
    </div>

    <!-- Timeline of Movements -->
    <div class="bg-bomberos-surface border border-bomberos-border rounded-3xl p-6 shadow-xl space-y-4">
      <div class="flex items-center justify-between border-b border-bomberos-border pb-3">
        <h3 class="text-xs font-bold text-gray-300 uppercase tracking-wider">Historial Auditado (Ledger Inmutable)</h3>
        <span class="text-xs text-gray-500 font-mono">{{ movimientosStore.movimientos.length }} registros</span>
      </div>

      <div v-if="movimientosStore.loading" class="text-center py-8 text-xs text-gray-400">
        Cargando bitácora de movimientos...
      </div>

      <div v-else-if="movimientosStore.movimientos.length === 0" class="text-center py-8 text-xs text-gray-400">
        No hay movimientos registrados.
      </div>

      <div v-else class="space-y-3">
        <div
          v-for="mov in movimientosStore.movimientos"
          :key="mov.id_movimiento"
          class="p-4 rounded-2xl bg-bomberos-card border border-bomberos-border hover:border-gray-500 transition-all flex flex-col md:flex-row md:items-center justify-between gap-4"
        >
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-bomberos-red/20 text-red-300 border border-red-800/40">
                {{ mov.tipo_movimiento_nombre }}
              </span>
              <span class="font-extrabold text-sm text-white">{{ mov.item_nombre }}</span>
              <span class="text-xs font-bold text-amber-400">({{ mov.cantidad }} unidades)</span>
            </div>

            <!-- Origin -> Destination Flow -->
            <div class="text-xs text-gray-300 flex items-center gap-2 pt-1">
              <span class="font-semibold text-gray-400">Origen:</span>
              <span class="px-2 py-0.5 rounded bg-bomberos-surface border border-bomberos-border text-gray-200">
                {{ mov.origen_nombre || 'NUEVA ADQUISICIÓN / ALTA' }}
              </span>
              <span>➔</span>
              <span class="font-semibold text-gray-400">Destino:</span>
              <span class="px-2 py-0.5 rounded bg-bomberos-surface border border-bomberos-border text-gray-200">
                {{ mov.destino_nombre || 'BAJA / CONSUMO DEFINITIVO' }}
              </span>
            </div>

            <p class="text-[11px] text-gray-400 pt-1">
              <strong class="text-gray-300">Auditoría:</strong> {{ mov.observaciones || 'Sin observaciones.' }}
            </p>
          </div>

          <div class="text-right shrink-0">
            <p class="text-xs font-bold text-gray-300">{{ mov.usuario_nombre }}</p>
            <p class="text-[10px] text-gray-500 font-mono">{{ new Date(mov.fecha).toLocaleString('es-CL') }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Nuevo Movimiento / Traslado -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div class="bg-bomberos-surface border border-bomberos-border rounded-3xl w-full max-w-lg overflow-hidden shadow-2xl p-6 space-y-4">
        <div class="flex items-center justify-between border-b border-bomberos-border pb-3">
          <h3 class="font-bold text-base text-white">Registrar Movimiento en Inventario</h3>
          <button @click="showModal = false" class="text-gray-400 hover:text-white font-bold">✕</button>
        </div>

        <form @submit.prevent="handleSubmitMovimiento" class="space-y-3">
          <!-- Ítem -->
          <div>
            <label class="block text-xs font-bold text-gray-400 mb-1">Bien / Material a Mover *</label>
            <select v-model.number="form.id_item" required class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-bomberos-red">
              <option v-for="item in catalogoStore.items" :key="item.id_item" :value="item.id_item">
                {{ item.nombre }} ({{ item.tipo_clasificacion }})
              </option>
            </select>
          </div>

          <!-- Tipo Movimiento -->
          <div>
            <label class="block text-xs font-bold text-gray-400 mb-1">Tipo de Movimiento *</label>
            <select v-model.number="form.id_tipo_mov" required class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-bomberos-red">
              <option v-for="tm in movimientosStore.tiposMovimiento" :key="tm.id_tipo_mov" :value="tm.id_tipo_mov">
                {{ tm.tipo_mov }}
              </option>
            </select>
          </div>

          <!-- Origen & Destino -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-bold text-gray-400 mb-1">Ubicación Origen</label>
              <select v-model.number="form.id_ubicacion_origen" class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-bomberos-red">
                <option :value="null">Ninguna (Alta/Compra)</option>
                <option v-for="ub in ubicacionesStore.ubicaciones" :key="ub.id_ubicacion" :value="ub.id_ubicacion">
                  {{ ub.nombre }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-bold text-gray-400 mb-1">Ubicación Destino</label>
              <select v-model.number="form.id_ubicacion_destino" class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-bomberos-red">
                <option :value="null">Ninguna (Baja/Extravío)</option>
                <option v-for="ub in ubicacionesStore.ubicaciones" :key="ub.id_ubicacion" :value="ub.id_ubicacion">
                  {{ ub.nombre }}
                </option>
              </select>
            </div>
          </div>

          <!-- Cantidad & Observaciones -->
          <div>
            <label class="block text-xs font-bold text-gray-400 mb-1">Cantidad a Mover *</label>
            <input
              v-model.number="form.cantidad"
              type="number"
              min="1"
              required
              class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-bomberos-red"
            />
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-400 mb-1">Motivo / Observaciones *</label>
            <textarea
              v-model="form.observaciones"
              rows="2"
              required
              placeholder="Ej. Reubicación para acto de servicio o reposición de bodega..."
              class="w-full bg-bomberos-card border border-bomberos-border rounded-xl p-3 text-xs text-white focus:outline-none focus:border-bomberos-red"
            ></textarea>
          </div>

          <div class="pt-3 border-t border-bomberos-border flex items-center justify-end gap-3">
            <button
              type="button"
              @click="showModal = false"
              class="px-4 py-2 rounded-xl border border-bomberos-border text-xs font-bold text-gray-300"
            >
              Cancelar
            </button>
            <button
              type="submit"
              class="px-5 py-2 rounded-xl bg-bomberos-red hover:bg-bomberos-red-hover text-white text-xs font-bold shadow-lg"
            >
              Ejecutar Traslado
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useCatalogoStore } from '../stores/catalogo'
import { useMovimientosStore } from '../stores/movimientos'
import { useUbicacionesStore } from '../stores/ubicaciones'

const movimientosStore = useMovimientosStore()
const catalogoStore = useCatalogoStore()
const ubicacionesStore = useUbicacionesStore()

const showModal = ref(false)

const form = reactive({
  id_item: 1,
  id_tipo_mov: 3, // TRASLADO
  id_ubicacion_origen: 12, // Bodega Pañol
  id_ubicacion_destino: 5, // Carro B-6 Cortina Izq 1
  cantidad: 2,
  observaciones: '',
})

onMounted(async () => {
  await Promise.all([
    movimientosStore.fetchMovimientos(),
    catalogoStore.fetchCatalogo(),
    ubicacionesStore.fetchUbicaciones(),
  ])
})

const handleSubmitMovimiento = async () => {
  const res = await movimientosStore.createMovimiento(form)
  if (res.success) {
    showModal.value = false
    await ubicacionesStore.fetchUbicaciones()
    alert('¡Movimiento ejecutado y registrado en el ledger inmutable con éxito!')
  } else {
    alert(res.error)
  }
}
</script>
