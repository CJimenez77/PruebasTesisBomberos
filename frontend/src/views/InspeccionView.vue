<template>
  <div class="p-6 space-y-6 max-w-5xl mx-auto">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-black text-white tracking-tight">Inspección Operativa & Post-Emergencia</h1>
        <p class="text-xs text-gray-400 mt-0.5">Recuento rápido de material tras retorno de acto de servicio</p>
      </div>

      <div class="flex items-center gap-2">
        <span class="text-xs px-3 py-1.5 rounded-xl bg-amber-950/80 border border-amber-800/60 text-amber-300 font-bold flex items-center gap-1.5">
          <span>⚠️</span> Detección Automática de Discrepancias
        </span>
      </div>
    </div>

    <!-- Form Configuration Card -->
    <div class="bg-bomberos-surface border border-bomberos-border rounded-3xl p-6 shadow-xl space-y-4">
      <h3 class="text-xs font-bold text-gray-300 uppercase tracking-wider">1. Parámetros de la Inspección</h3>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div>
          <label class="block text-xs font-bold text-gray-400 mb-1">Unidad a Inspeccionar *</label>
          <select
            v-model.number="selectedUnidadId"
            @change="loadChecklist"
            class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-bomberos-red"
          >
            <option :value="1">Carro Bomba B-6 (Ataque)</option>
            <option :value="2">Unidad de Rescate R-6</option>
            <option :value="3">Bodega Central Cuartel</option>
          </select>
        </div>

        <div>
          <label class="block text-xs font-bold text-gray-400 mb-1">Tipo de Evento *</label>
          <select
            v-model.number="tipoInspeccionId"
            class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-bomberos-red"
          >
            <option :value="2">Post-Emergencia (Retorno Acto de Servicio)</option>
            <option :value="1">Rutinaria Periódica / Semanal</option>
          </select>
        </div>

        <div>
          <label class="block text-xs font-bold text-gray-400 mb-1">Inspector Responsable</label>
          <input
            type="text"
            :value="authStore.userName + ' (' + authStore.userRole + ')'"
            disabled
            class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-3 py-2 text-xs text-gray-400 font-semibold cursor-not-allowed"
          />
        </div>
      </div>
    </div>

    <!-- Checklist Items -->
    <div class="bg-bomberos-surface border border-bomberos-border rounded-3xl p-6 shadow-xl space-y-4">
      <div class="flex items-center justify-between border-b border-bomberos-border pb-3">
        <h3 class="text-xs font-bold text-gray-300 uppercase tracking-wider">2. Recuento de Herramientas & Material Asignado</h3>
        <button
          @click="resetToExpected"
          class="text-xs font-bold text-bomberos-red hover:underline"
        >
          Resetear todo a stock esperado
        </button>
      </div>

      <div v-if="loadingItems" class="text-center py-8 text-xs text-gray-400">
        Cargando material asignado a la unidad...
      </div>

      <div v-else-if="itemsChecklist.length === 0" class="text-center py-8 text-xs text-gray-400">
        No hay herramientas registradas para esta unidad.
      </div>

      <div v-else class="space-y-3">
        <div
          v-for="item in itemsChecklist"
          :key="item.id_item + '-' + item.id_ubicacion"
          class="p-4 rounded-2xl bg-bomberos-card border transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4"
          :class="item.encontrado < item.esperado ? 'border-red-600/80 bg-red-950/20' : 'border-bomberos-border'"
        >
          <div>
            <div class="flex items-center gap-2">
              <span class="font-extrabold text-sm text-white">{{ item.nombre }}</span>
              <span class="text-[10px] px-2 py-0.5 rounded bg-bomberos-surface border border-bomberos-border text-gray-400 font-mono">
                {{ item.ubicacion_nombre }}
              </span>
            </div>
            <p class="text-xs text-gray-400 mt-0.5">Stock teórico esperado: <strong class="text-gray-200">{{ item.esperado }}</strong></p>
          </div>

          <!-- Counter controls -->
          <div class="flex items-center gap-4">
            <div class="flex items-center bg-bomberos-surface border border-bomberos-border rounded-xl p-1">
              <button
                @click="item.encontrado = Math.max(0, item.encontrado - 1)"
                class="w-8 h-8 rounded-lg bg-bomberos-card hover:bg-bomberos-border text-white font-bold flex items-center justify-center transition-colors"
              >
                −
              </button>
              <span class="w-12 text-center font-black text-base text-white">
                {{ item.encontrado }}
              </span>
              <button
                @click="item.encontrado++"
                class="w-8 h-8 rounded-lg bg-bomberos-card hover:bg-bomberos-border text-white font-bold flex items-center justify-center transition-colors"
              >
                +
              </button>
            </div>

            <!-- Discrepancy indicator -->
            <div class="w-28 text-right">
              <span
                v-if="item.encontrado < item.esperado"
                class="text-xs font-bold text-red-400 bg-red-950/90 border border-red-800 px-2.5 py-1 rounded-lg block"
              >
                Faltan {{ item.esperado - item.encontrado }}
              </span>
              <span
                v-else-if="item.encontrado > item.esperado"
                class="text-xs font-bold text-amber-400 bg-amber-950/90 border border-amber-800 px-2.5 py-1 rounded-lg block"
              >
                +{{ item.encontrado - item.esperado }} extra
              </span>
              <span
                v-else
                class="text-xs font-bold text-emerald-400 bg-emerald-950/90 border border-emerald-800 px-2.5 py-1 rounded-lg block"
              >
                ✓ Conforme
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Footer -->
      <div class="pt-4 border-t border-bomberos-border flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div class="text-xs text-gray-400">
          <span v-if="hasDiscrepancies" class="text-red-400 font-bold">
            ⚠️ Se generará automáticamente una ALERTA DE DISCREPANCIA para el Capitán y Director.
          </span>
          <span v-else class="text-emerald-400 font-bold">
            ✓ Todo el material coincide con el saldo de inventario.
          </span>
        </div>

        <button
          @click="saveInspection"
          :disabled="isSubmitting || itemsChecklist.length === 0"
          class="px-6 py-3 rounded-xl bg-bomberos-red hover:bg-bomberos-red-hover text-white text-sm font-bold shadow-xl shadow-red-950/50 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
        >
          <span>💾</span> {{ isSubmitting ? 'Guardando...' : 'Registrar y Finalizar Inspección' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../api/client'
import { useAuthStore } from '../stores/auth'
import { useInspeccionesStore } from '../stores/inspecciones'
import { useUbicacionesStore } from '../stores/ubicaciones'

const authStore = useAuthStore()
const inspeccionesStore = useInspeccionesStore()
const ubicacionesStore = useUbicacionesStore()
const router = useRouter()

const selectedUnidadId = ref(1) // B-6 por defecto
const tipoInspeccionId = ref(2) // POST_EMERGENCIA
const itemsChecklist = ref([])
const loadingItems = ref(false)
const isSubmitting = ref(false)

const loadChecklist = async () => {
  loadingItems.value = true
  try {
    await ubicacionesStore.fetchUbicaciones()
    const subs = ubicacionesStore.ubicaciones.filter(u => u.id_ubicacion_padre === selectedUnidadId.value)
    const promises = subs.map(s => apiClient.get(`/ubicaciones/${s.id_ubicacion}/stock`))
    const results = await Promise.all(promises)
    const combined = results.flatMap(r => r.data)

    itemsChecklist.value = combined.map(item => ({
      id_item: item.id_item,
      id_ubicacion: item.id_ubicacion,
      nombre: item.item_nombre,
      ubicacion_nombre: item.ubicacion_nombre,
      esperado: item.cantidad_asignada,
      encontrado: item.cantidad_asignada,
      estado: 'OPERATIVO'
    }))
  } catch (err) {
    console.error(err)
  } finally {
    loadingItems.value = false
  }
}

const hasDiscrepancies = computed(() => {
  return itemsChecklist.value.some(i => i.encontrado !== i.esperado)
})

const resetToExpected = () => {
  itemsChecklist.value.forEach(i => {
    i.encontrado = i.esperado
  })
}

const saveInspection = async () => {
  isSubmitting.value = true
  const payload = {
    id_tipo_inspeccion: tipoInspeccionId.value,
    id_ubicacion: selectedUnidadId.value,
    detalles: itemsChecklist.value.map(i => ({
      id_item: i.id_item,
      cantidad_encontrada: i.encontrado,
      cantidad_teorica_actual: i.esperado,
      estado_reportado: i.estado,
    }))
  }

  const res = await inspeccionesStore.createInspeccion(payload)
  isSubmitting.value = false

  if (res.success) {
    alert('¡Inspección registrada con éxito! Si hubo discrepancias, la alerta fue generada automáticamente.')
    router.push('/alertas')
  } else {
    alert(res.error)
  }
}

onMounted(async () => {
  await loadChecklist()
})
</script>
