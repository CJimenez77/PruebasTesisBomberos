<template>
  <div class="p-6 space-y-6 max-w-7xl mx-auto">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-black text-white tracking-tight">Carros y Ubicaciones del Cuartel</h1>
        <p class="text-xs text-gray-400 mt-0.5">Jerarquía de unidades vehiculares, bodegas y material asignado</p>
      </div>

      <router-link
        to="/movimientos"
        class="px-4 py-2.5 rounded-xl bg-bomberos-red hover:bg-bomberos-red-hover text-white text-xs font-bold shadow-lg shadow-red-950/40 transition-all flex items-center gap-2"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
        </svg>
        <span>Trasladar Material</span>
      </router-link>
    </div>

    <!-- Units Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
      <!-- Carro B-6 -->
      <div
        @click="selectCarro(1, 'Carro Bomba B-6')"
        class="bg-bomberos-card border rounded-3xl p-5 cursor-pointer transition-all duration-200 hover:scale-[1.01]"
        :class="activeCarroId === 1 ? 'border-bomberos-red shadow-xl shadow-red-950/40 bg-bomberos-surface' : 'border-bomberos-border hover:border-gray-500'"
      >
        <div class="flex items-center justify-between mb-3">
          <div class="w-10 h-10 rounded-xl bg-red-950 border border-red-800/60 flex items-center justify-center text-red-400 font-bold">
            B-6
          </div>
          <span class="text-[10px] font-extrabold px-2.5 py-1 rounded-lg bg-emerald-950 text-emerald-400 border border-emerald-800/60 uppercase">
            OPERATIVO
          </span>
        </div>
        <h3 class="font-black text-lg text-white">Carro Bomba B-6</h3>
        <p class="text-xs text-gray-400 mt-1">Unidad de agua y ataque de primera intervención (Renault Camiva).</p>
        <div class="mt-4 pt-3 border-t border-bomberos-border/60 flex items-center justify-between text-xs">
          <span class="text-gray-400">5 Cortinas / Gavetas</span>
          <span class="font-bold text-red-400">Ver inventario</span>
        </div>
      </div>

      <!-- Carro R-6 -->
      <div
        @click="selectCarro(2, 'Unidad de Rescate R-6')"
        class="bg-bomberos-card border rounded-3xl p-5 cursor-pointer transition-all duration-200 hover:scale-[1.01]"
        :class="activeCarroId === 2 ? 'border-bomberos-red shadow-xl shadow-red-950/40 bg-bomberos-surface' : 'border-bomberos-border hover:border-gray-500'"
      >
        <div class="flex items-center justify-between mb-3">
          <div class="w-10 h-10 rounded-xl bg-red-950 border border-red-800/60 flex items-center justify-center text-red-400 font-bold">
            R-6
          </div>
          <span class="text-[10px] font-extrabold px-2.5 py-1 rounded-lg bg-emerald-950 text-emerald-400 border border-emerald-800/60 uppercase">
            OPERATIVO
          </span>
        </div>
        <h3 class="font-black text-lg text-white">Unidad de Rescate R-6</h3>
        <p class="text-xs text-gray-400 mt-1">Rescate vehicular, extricación pesada y cuerdas.</p>
        <div class="mt-4 pt-3 border-t border-bomberos-border/60 flex items-center justify-between text-xs">
          <span class="text-gray-400">4 Compartimentos</span>
          <span class="font-bold text-red-400">Ver inventario</span>
        </div>
      </div>

      <!-- Bodega Central Cuartel -->
      <div
        @click="selectCarro(3, 'Bodega Central del Cuartel')"
        class="bg-bomberos-card border rounded-3xl p-5 cursor-pointer transition-all duration-200 hover:scale-[1.01]"
        :class="activeCarroId === 3 ? 'border-bomberos-red shadow-xl shadow-red-950/40 bg-bomberos-surface' : 'border-bomberos-border hover:border-gray-500'"
      >
        <div class="flex items-center justify-between mb-3">
          <div class="w-10 h-10 rounded-xl bg-blue-950 border border-blue-800/60 flex items-center justify-center text-blue-400 font-bold">
            BOD
          </div>
          <span class="text-[10px] font-extrabold px-2.5 py-1 rounded-lg bg-blue-950 text-blue-400 border border-blue-800/60 uppercase">
            CENTRAL
          </span>
        </div>
        <h3 class="font-black text-lg text-white">Bodega Central Cuartel</h3>
        <p class="text-xs text-gray-400 mt-1">Stock de reserva, insumos médicos y pañol de repuestos.</p>
        <div class="mt-4 pt-3 border-t border-bomberos-border/60 flex items-center justify-between text-xs">
          <span class="text-gray-400">3 Estantes / Pañol</span>
          <span class="font-bold text-red-400">Ver inventario</span>
        </div>
      </div>
    </div>

    <!-- Active Unit Detail & Stock Table -->
    <div class="bg-bomberos-surface border border-bomberos-border rounded-3xl p-6 shadow-xl space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-bomberos-border pb-4">
        <div>
          <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Inventario en Vivo</span>
          <h2 class="text-xl font-black text-white">{{ activeCarroName }}</h2>
        </div>
        <div class="text-xs text-gray-400 bg-bomberos-card px-3 py-1.5 rounded-xl border border-bomberos-border">
          Relación Reflexiva Jerárquica MER v3
        </div>
      </div>

      <!-- Sub-locations / Compartments list -->
      <div>
        <h4 class="text-xs font-bold text-gray-300 uppercase tracking-wider mb-2">Compartimentos / Zonas Registradas:</h4>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="sub in subUbicaciones"
            :key="sub.id_ubicacion"
            @click="fetchSubStock(sub.id_ubicacion)"
            class="px-3 py-1.5 rounded-xl text-xs font-bold border transition-all"
            :class="activeSubId === sub.id_ubicacion ? 'bg-bomberos-red text-white border-bomberos-red' : 'bg-bomberos-card text-gray-300 border-bomberos-border hover:border-gray-400'"
          >
            {{ sub.nombre }}
          </button>
        </div>
      </div>

      <!-- Stock Table Preview -->
      <div class="overflow-x-auto pt-2">
        <div v-if="loadingStock" class="text-center py-8 text-xs text-gray-400">
          Cargando inventario asignado...
        </div>
        <div v-else-if="stockList.length === 0" class="text-center py-8 text-xs text-gray-400">
          No hay ítems asignados directamente a esta gaveta/ubicación.
        </div>
        <table v-else class="w-full text-left text-xs text-gray-300">
          <thead class="bg-bomberos-card text-gray-400 uppercase text-[10px] tracking-wider font-extrabold">
            <tr>
              <th class="px-4 py-3 rounded-l-xl">Material / Bien</th>
              <th class="px-4 py-3">Ubicación Fisiológica</th>
              <th class="px-4 py-3 text-right rounded-r-xl">Cantidad Asignada</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-bomberos-border/40">
            <tr v-for="stk in stockList" :key="stk.id_item + '-' + stk.id_ubicacion" class="hover:bg-white/5 transition-colors">
              <td class="px-4 py-3 font-bold text-gray-100">
                {{ stk.item_nombre }}
              </td>
              <td class="px-4 py-3 text-gray-400">{{ stk.ubicacion_nombre }}</td>
              <td class="px-4 py-3 text-right font-extrabold text-white">{{ stk.cantidad_asignada }} unidades</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import apiClient from '../api/client'
import { useUbicacionesStore } from '../stores/ubicaciones'

const ubicacionesStore = useUbicacionesStore()
const activeCarroId = ref(1)
const activeCarroName = ref('Carro Bomba B-6')
const activeSubId = ref(null)
const stockList = ref([])
const loadingStock = ref(false)

const subUbicaciones = computed(() => {
  return ubicacionesStore.ubicaciones.filter(u => u.id_ubicacion_padre === activeCarroId.value)
})

const selectCarro = async (id, name) => {
  activeCarroId.value = id
  activeCarroName.value = name
  activeSubId.value = null
  await fetchAllSubStock(id)
}

const fetchSubStock = async (subId) => {
  activeSubId.value = subId
  loadingStock.value = true
  try {
    const res = await apiClient.get(`/ubicaciones/${subId}/stock`)
    stockList.value = res.data
  } catch (err) {
    console.error(err)
  } finally {
    loadingStock.value = false
  }
}

const fetchAllSubStock = async (parentId) => {
  loadingStock.value = true
  try {
    const subs = ubicacionesStore.ubicaciones.filter(u => u.id_ubicacion_padre === parentId)
    const promises = subs.map(s => apiClient.get(`/ubicaciones/${s.id_ubicacion}/stock`))
    const results = await Promise.all(promises)
    const combined = results.flatMap(r => r.data)
    stockList.value = combined
  } catch (err) {
    console.error(err)
  } finally {
    loadingStock.value = false
  }
}

onMounted(async () => {
  await ubicacionesStore.fetchUbicaciones()
  await fetchAllSubStock(1)
})
</script>
