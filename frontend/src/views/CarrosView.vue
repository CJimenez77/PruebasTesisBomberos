<template>
  <div class="p-6 space-y-6 max-w-7xl mx-auto">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-black text-white tracking-tight">Carros y Ubicaciones del Cuartel</h1>
        <p class="text-xs text-gray-400 mt-0.5">Jerarquía de unidades vehiculares, bodegas y material asignado</p>
      </div>
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
          <div class="w-12 h-12 rounded-2xl bg-red-950 border border-red-800/60 flex items-center justify-center text-2xl">
            🚒
          </div>
          <span class="text-xs font-extrabold px-2.5 py-1 rounded-lg bg-emerald-950 text-emerald-400 border border-emerald-800/60">
            OPERATIVO
          </span>
        </div>
        <h3 class="font-black text-lg text-white">Carro Bomba B-6</h3>
        <p class="text-xs text-gray-400 mt-1">Unidad de agua y ataque de primera intervención.</p>
        <div class="mt-4 pt-3 border-t border-bomberos-border/60 flex items-center justify-between text-xs">
          <span class="text-gray-400">4 Cortinas / Gavetas</span>
          <span class="font-bold text-red-400">Ver inventario →</span>
        </div>
      </div>

      <!-- Carro R-6 -->
      <div
        @click="selectCarro(2, 'Unidad de Rescate R-6')"
        class="bg-bomberos-card border rounded-3xl p-5 cursor-pointer transition-all duration-200 hover:scale-[1.01]"
        :class="activeCarroId === 2 ? 'border-bomberos-red shadow-xl shadow-red-950/40 bg-bomberos-surface' : 'border-bomberos-border hover:border-gray-500'"
      >
        <div class="flex items-center justify-between mb-3">
          <div class="w-12 h-12 rounded-2xl bg-red-950 border border-red-800/60 flex items-center justify-center text-2xl">
            🚑
          </div>
          <span class="text-xs font-extrabold px-2.5 py-1 rounded-lg bg-emerald-950 text-emerald-400 border border-emerald-800/60">
            OPERATIVO
          </span>
        </div>
        <h3 class="font-black text-lg text-white">Unidad de Rescate R-6</h3>
        <p class="text-xs text-gray-400 mt-1">Rescate vehicular, extricación y trauma.</p>
        <div class="mt-4 pt-3 border-t border-bomberos-border/60 flex items-center justify-between text-xs">
          <span class="text-gray-400">3 Gavetas / Maletero</span>
          <span class="font-bold text-red-400">Ver inventario →</span>
        </div>
      </div>

      <!-- Bodega Central Cuartel -->
      <div
        @click="selectCarro(3, 'Bodega Central del Cuartel')"
        class="bg-bomberos-card border rounded-3xl p-5 cursor-pointer transition-all duration-200 hover:scale-[1.01]"
        :class="activeCarroId === 3 ? 'border-bomberos-red shadow-xl shadow-red-950/40 bg-bomberos-surface' : 'border-bomberos-border hover:border-gray-500'"
      >
        <div class="flex items-center justify-between mb-3">
          <div class="w-12 h-12 rounded-2xl bg-amber-950 border border-amber-800/60 flex items-center justify-center text-2xl">
            🏢
          </div>
          <span class="text-xs font-extrabold px-2.5 py-1 rounded-lg bg-blue-950 text-blue-400 border border-blue-800/60">
            CENTRAL
          </span>
        </div>
        <h3 class="font-black text-lg text-white">Bodega Central Cuartel</h3>
        <p class="text-xs text-gray-400 mt-1">Stock de reserva, insumos médicos y pañol de repuestos.</p>
        <div class="mt-4 pt-3 border-t border-bomberos-border/60 flex items-center justify-between text-xs">
          <span class="text-gray-400">Estantes & Pañol</span>
          <span class="font-bold text-red-400">Ver inventario →</span>
        </div>
      </div>
    </div>

    <!-- Active Unit Detail & Stock Table -->
    <div class="bg-bomberos-surface border border-bomberos-border rounded-3xl p-6 shadow-xl space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-bomberos-border pb-4">
        <div>
          <span class="text-xs font-bold text-bomberos-gold uppercase tracking-wider">Detalle de Ubicación</span>
          <h2 class="text-xl font-black text-white">{{ activeCarroName }}</h2>
        </div>
        <div class="text-xs text-gray-400 bg-bomberos-card px-3 py-1.5 rounded-xl border border-bomberos-border">
          Relación Reflexiva Jerárquica MER v3
        </div>
      </div>

      <!-- Sub-locations / Compartments buttons -->
      <div>
        <h4 class="text-xs font-bold text-gray-300 uppercase tracking-wider mb-2">Compartimentos / Gavetas:</h4>
        <div class="flex flex-wrap gap-2">
          <button
            class="px-3 py-1.5 rounded-xl text-xs font-bold bg-bomberos-red text-white shadow"
          >
            Vista General (Todo el Carro)
          </button>
          <button
            class="px-3 py-1.5 rounded-xl text-xs font-bold bg-bomberos-card text-gray-300 border border-bomberos-border hover:border-gray-400"
          >
            Cabina de Conducción
          </button>
          <button
            class="px-3 py-1.5 rounded-xl text-xs font-bold bg-bomberos-card text-gray-300 border border-bomberos-border hover:border-gray-400"
          >
            Cortina Izquierda 1 (Ataque)
          </button>
          <button
            class="px-3 py-1.5 rounded-xl text-xs font-bold bg-bomberos-card text-gray-300 border border-bomberos-border hover:border-gray-400"
          >
            Cortina Derecha 1 (Alimentación)
          </button>
          <button
            class="px-3 py-1.5 rounded-xl text-xs font-bold bg-bomberos-card text-gray-300 border border-bomberos-border hover:border-gray-400"
          >
            Techo / Escalas
          </button>
        </div>
      </div>

      <!-- Stock Table Preview -->
      <div class="overflow-x-auto pt-2">
        <table class="w-full text-left text-xs text-gray-300">
          <thead class="bg-bomberos-card text-gray-400 uppercase text-[10px] tracking-wider font-extrabold">
            <tr>
              <th class="px-4 py-3 rounded-l-xl">Material / Bien</th>
              <th class="px-4 py-3">Tipo Clasificación</th>
              <th class="px-4 py-3">Estado</th>
              <th class="px-4 py-3 text-right rounded-r-xl">Cantidad Asignada</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-bomberos-border/40">
            <tr class="hover:bg-white/5 transition-colors">
              <td class="px-4 py-3 font-bold text-gray-100 flex items-center gap-2">
                <span>🧯</span> Extintor PQS 10kg ABC
              </td>
              <td class="px-4 py-3 font-mono text-[11px] text-amber-300">QR-EXT-001 (Unitario)</td>
              <td class="px-4 py-3">
                <span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 font-bold text-[10px]">OPERATIVO</span>
              </td>
              <td class="px-4 py-3 text-right font-extrabold text-white">1 unidad</td>
            </tr>
            <tr class="hover:bg-white/5 transition-colors">
              <td class="px-4 py-3 font-bold text-gray-100 flex items-center gap-2">
                <span>🌊</span> Manguera Sintética 70mm x 25m
              </td>
              <td class="px-4 py-3 text-gray-400">Agrupable / Por Lote</td>
              <td class="px-4 py-3">
                <span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 font-bold text-[10px]">OPERATIVO</span>
              </td>
              <td class="px-4 py-3 text-right font-extrabold text-white">12 unidades</td>
            </tr>
            <tr class="hover:bg-white/5 transition-colors">
              <td class="px-4 py-3 font-bold text-gray-100 flex items-center gap-2">
                <span>🪓</span> Hacha de Bombero Pico-Plana
              </td>
              <td class="px-4 py-3 text-gray-400">Agrupable / Por Lote</td>
              <td class="px-4 py-3">
                <span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 font-bold text-[10px]">OPERATIVO</span>
              </td>
              <td class="px-4 py-3 text-right font-extrabold text-white">2 unidades</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useUbicacionesStore } from '../stores/ubicaciones'

const ubicacionesStore = useUbicacionesStore()
const activeCarroId = ref(1)
const activeCarroName = ref('Carro Bomba B-6')

const selectCarro = (id, name) => {
  activeCarroId.value = id
  activeCarroName.value = name
  ubicacionesStore.fetchStock(id)
}

onMounted(async () => {
  await ubicacionesStore.fetchUbicaciones()
})
</script>
