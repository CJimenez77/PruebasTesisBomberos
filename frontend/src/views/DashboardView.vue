<template>
  <div class="p-6 space-y-6 max-w-7xl mx-auto">
    <!-- Critical Alert Banner if there are pending alerts -->
    <div
      v-if="summary.alertas_pendientes > 0"
      class="bg-red-950/80 border border-red-600/80 p-5 rounded-3xl shadow-xl flex flex-col sm:flex-row sm:items-center justify-between gap-4 animate-in fade-in"
    >
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-red-600 text-white flex items-center justify-center font-bold">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
          </svg>
        </div>
        <div>
          <h3 class="font-extrabold text-sm text-red-200 uppercase tracking-wide">
            Atención Mando: {{ summary.alertas_pendientes }} discrepancia(s) crítica(s) pendiente(s) de revisión
          </h3>
          <p class="text-xs text-red-300/80 mt-0.5">
            Diferencias de material detectadas tras el retorno de acto de servicio en las unidades.
          </p>
        </div>
      </div>

      <router-link
        to="/alertas"
        class="px-4 py-2 bg-red-600 hover:bg-red-500 text-white text-xs font-bold rounded-xl shadow-lg transition-all shrink-0 text-center uppercase tracking-wider"
      >
        Revisar y Visar Alertas
      </router-link>
    </div>

    <!-- Welcome Header -->
    <div class="bg-gradient-to-r from-bomberos-surface via-bomberos-card to-bomberos-surface border border-bomberos-border p-6 rounded-3xl shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="text-[10px] font-extrabold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-bomberos-red text-white">
            {{ authStore.userRole }}
          </span>
          <span class="text-xs text-gray-400">Sesión Institucional Activa</span>
        </div>
        <h1 class="text-2xl font-black text-white mt-1">
          Bienvenido, {{ authStore.userName }}
        </h1>
        <p class="text-xs text-gray-400 mt-0.5">
          Sistema de Control de Inventario y Trazabilidad Operativa — Cuartel 6ta Compañía
        </p>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <router-link
          to="/catalogo"
          class="px-4 py-2.5 rounded-xl bg-bomberos-red hover:bg-bomberos-red-hover text-white text-xs font-bold shadow-lg shadow-red-950/40 transition-all flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
          </svg>
          <span>Catálogo</span>
        </router-link>
        <router-link
          to="/movimientos"
          class="px-4 py-2.5 rounded-xl bg-bomberos-card hover:bg-bomberos-border text-gray-200 border border-bomberos-border text-xs font-bold transition-all flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          <span>Traslados</span>
        </router-link>
        <router-link
          to="/inspeccion"
          class="px-4 py-2.5 rounded-xl bg-bomberos-card hover:bg-bomberos-border text-gray-200 border border-bomberos-border text-xs font-bold transition-all flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
          </svg>
          <span>Inspección</span>
        </router-link>
      </div>
    </div>

    <!-- 4 Stats Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Total Items -->
      <div class="bg-bomberos-card border border-bomberos-border p-5 rounded-2xl shadow-lg">
        <div class="flex items-center justify-between text-gray-400 mb-2">
          <span class="text-xs font-bold uppercase tracking-wider">Total Bienes Registrados</span>
          <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
          </svg>
        </div>
        <div class="text-3xl font-black text-white">{{ summary.total_items }}</div>
        <p class="text-xs text-gray-400 mt-1">{{ summary.total_unidades_stock }} unidades en existencia total</p>
      </div>

      <!-- Unidades / Carros -->
      <div class="bg-bomberos-card border border-bomberos-border p-5 rounded-2xl shadow-lg">
        <div class="flex items-center justify-between text-gray-400 mb-2">
          <span class="text-xs font-bold uppercase tracking-wider">Unidades Operativas</span>
          <svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"></path>
          </svg>
        </div>
        <div class="text-3xl font-black text-emerald-400">{{ summary.total_carros }}</div>
        <p class="text-xs text-gray-400 mt-1">Carros Bomba B-6 y R-6 en servicio</p>
      </div>

      <!-- Alertas Discrepancia -->
      <div class="bg-bomberos-card border border-bomberos-border p-5 rounded-2xl shadow-lg">
        <div class="flex items-center justify-between text-gray-400 mb-2">
          <span class="text-xs font-bold uppercase tracking-wider">Alertas Pendientes</span>
          <svg class="w-5 h-5" :class="summary.alertas_pendientes > 0 ? 'text-red-400' : 'text-emerald-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
          </svg>
        </div>
        <div class="text-3xl font-black" :class="summary.alertas_pendientes > 0 ? 'text-red-400' : 'text-emerald-400'">
          {{ summary.alertas_pendientes }}
        </div>
        <p class="text-xs text-gray-400 mt-1">Diferencias activas por auditar</p>
      </div>

      <!-- Motor DB Status -->
      <div class="bg-bomberos-card border border-bomberos-border p-5 rounded-2xl shadow-lg">
        <div class="flex items-center justify-between text-gray-400 mb-2">
          <span class="text-xs font-bold uppercase tracking-wider">Motor de Datos</span>
          <span class="text-xs font-mono font-bold text-gray-400">v16</span>
        </div>
        <div class="text-xl font-extrabold text-emerald-400 flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
          PostgreSQL Activo
        </div>
        <p class="text-xs text-gray-400 mt-2">15 Tablas relacionales MER v3</p>
      </div>
    </div>

    <!-- Quick Sections Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Carros Preview -->
      <div class="lg:col-span-2 bg-bomberos-surface border border-bomberos-border rounded-3xl p-6 shadow-xl space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <h2 class="font-black text-sm uppercase tracking-wider text-gray-100">Unidades Vehiculares y Cuartel</h2>
          </div>
          <router-link to="/carros" class="text-xs font-bold text-bomberos-red hover:underline">
            Explorar todas
          </router-link>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="p-4 rounded-2xl bg-bomberos-card border border-bomberos-border hover:border-bomberos-red/60 transition-all">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-extrabold px-2.5 py-1 rounded-lg bg-emerald-950 text-emerald-400 border border-emerald-800/60 uppercase">
                OPERATIVO
              </span>
              <span class="text-xs text-gray-400 font-medium">1ra Intervención</span>
            </div>
            <h3 class="text-base font-black text-white mt-2">Carro Bomba B-6</h3>
            <p class="text-xs text-gray-400 mt-1">5 Gavetas y compartimentos de mangueras, pitones y agua</p>
            <router-link to="/carros" class="inline-block mt-3 text-xs font-bold text-red-400 hover:text-red-300">
              Ver compartimentos y stock
            </router-link>
          </div>

          <div class="p-4 rounded-2xl bg-bomberos-card border border-bomberos-border hover:border-bomberos-red/60 transition-all">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-extrabold px-2.5 py-1 rounded-lg bg-emerald-950 text-emerald-400 border border-emerald-800/60 uppercase">
                OPERATIVO
              </span>
              <span class="text-xs text-gray-400 font-medium">Rescate Pesado</span>
            </div>
            <h3 class="text-base font-black text-white mt-2">Unidad de Rescate R-6</h3>
            <p class="text-xs text-gray-400 mt-1">Herramientas hidráulicas Holmatro, cojines Vetter y cuerdas</p>
            <router-link to="/carros" class="inline-block mt-3 text-xs font-bold text-red-400 hover:text-red-300">
              Ver compartimentos y stock
            </router-link>
          </div>
        </div>
      </div>

      <!-- Últimas Alertas Activas -->
      <div class="bg-bomberos-surface border border-bomberos-border rounded-3xl p-6 shadow-xl flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-black text-sm uppercase tracking-wider text-gray-100">Alertas Recientes</h2>
            <router-link to="/alertas" class="text-xs font-bold text-bomberos-red hover:underline">
              Ver todas
            </router-link>
          </div>

          <div v-if="summary.ultimas_alertas.length === 0" class="text-center py-6 text-xs text-gray-400">
            No hay discrepancias pendientes registradas.
          </div>

          <div v-else class="space-y-2.5">
            <div
              v-for="alt in summary.ultimas_alertas"
              :key="alt.id_alerta"
              class="p-3 rounded-xl bg-red-950/30 border border-red-800/60 text-xs space-y-1"
            >
              <div class="flex items-center justify-between">
                <span class="font-bold text-white">{{ alt.item_nombre }}</span>
                <span class="text-red-400 font-extrabold">{{ alt.diferencia }} u.</span>
              </div>
              <p class="text-[11px] text-gray-400 truncate">{{ alt.ubicacion_nombre }} — {{ alt.observaciones }}</p>
            </div>
          </div>
        </div>

        <div class="pt-4 mt-4 border-t border-bomberos-border/60 text-center">
          <router-link to="/alertas" class="text-xs font-bold text-bomberos-red hover:underline uppercase tracking-wider">
            Ir al panel de resolución
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive } from 'vue'
import apiClient from '../api/client'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const summary = reactive({
  total_items: 26,
  total_unidades_stock: 120,
  total_carros: 2,
  alertas_pendientes: 1,
  inspecciones_count: 1,
  ultimas_alertas: [],
})

onMounted(async () => {
  try {
    const res = await apiClient.get('/dashboard/resumen')
    Object.assign(summary, res.data)
  } catch (err) {
    console.error('Error fetching dashboard summary', err)
  }
})
</script>
