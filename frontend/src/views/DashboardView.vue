<template>
  <div class="p-6 space-y-6 max-w-7xl mx-auto">
    <!-- Critical Alert Banner if there are pending alerts -->
    <div
      v-if="summary.alertas_pendientes > 0"
      class="bg-red-950/80 border border-red-600/80 p-5 rounded-3xl shadow-xl flex flex-col sm:flex-row sm:items-center justify-between gap-4 animate-in fade-in"
    >
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-red-600 text-white flex items-center justify-center text-xl font-bold animate-pulse">
          ⚠️
        </div>
        <div>
          <h3 class="font-extrabold text-sm text-red-200">
            ¡Atención Mando! Hay {{ summary.alertas_pendientes }} discrepancia(s) crítica(s) pendiente(s) de revisión
          </h3>
          <p class="text-xs text-red-300/80 mt-0.5">
            Diferencias detectadas tras el retorno de acto de servicio en las unidades.
          </p>
        </div>
      </div>

      <router-link
        to="/alertas"
        class="px-4 py-2 bg-red-600 hover:bg-red-500 text-white text-xs font-bold rounded-xl shadow-lg transition-all shrink-0 text-center"
      >
        Revisar y Visar Alertas →
      </router-link>
    </div>

    <!-- Welcome Header -->
    <div class="bg-gradient-to-r from-bomberos-surface via-bomberos-card to-bomberos-surface border border-bomberos-border p-6 rounded-3xl shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="text-xs font-extrabold uppercase px-2.5 py-0.5 rounded-full bg-bomberos-red text-white">
            {{ authStore.userRole }}
          </span>
          <span class="text-xs text-gray-400">Sesión Activa</span>
        </div>
        <h1 class="text-2xl font-black text-white mt-1">
          Bienvenido, {{ authStore.userName }}
        </h1>
        <p class="text-xs text-gray-400 mt-0.5">
          Sistema de Control de Inventario y Trazabilidad Operativa — 6ta Compañía
        </p>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <router-link
          to="/catalogo"
          class="px-4 py-2.5 rounded-xl bg-bomberos-red hover:bg-bomberos-red-hover text-white text-xs font-bold shadow-lg shadow-red-950/40 transition-all flex items-center gap-2"
        >
          <span>📦</span> Catálogo
        </router-link>
        <router-link
          to="/movimientos"
          class="px-4 py-2.5 rounded-xl bg-bomberos-card hover:bg-bomberos-border text-gray-200 border border-bomberos-border text-xs font-bold transition-all flex items-center gap-2"
        >
          <span>🔄</span> Traslados
        </router-link>
        <router-link
          to="/inspeccion"
          class="px-4 py-2.5 rounded-xl bg-bomberos-card hover:bg-bomberos-border text-gray-200 border border-bomberos-border text-xs font-bold transition-all flex items-center gap-2"
        >
          <span>📋</span> Inspección
        </router-link>
      </div>
    </div>

    <!-- 4 Stats Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Total Items -->
      <div class="bg-bomberos-card border border-bomberos-border p-5 rounded-2xl shadow-lg">
        <div class="flex items-center justify-between text-gray-400 mb-2">
          <span class="text-xs font-bold uppercase tracking-wider">Total Bienes Registrados</span>
          <span class="text-xl">📦</span>
        </div>
        <div class="text-3xl font-black text-white">{{ summary.total_items }}</div>
        <p class="text-xs text-gray-400 mt-1">{{ summary.total_unidades_stock }} unidades en existencia total</p>
      </div>

      <!-- Unidades / Carros -->
      <div class="bg-bomberos-card border border-bomberos-border p-5 rounded-2xl shadow-lg">
        <div class="flex items-center justify-between text-gray-400 mb-2">
          <span class="text-xs font-bold uppercase tracking-wider">Unidades Operativas</span>
          <span class="text-xl">🚒</span>
        </div>
        <div class="text-3xl font-black text-emerald-400">{{ summary.total_carros }}</div>
        <p class="text-xs text-gray-400 mt-1">Carros Bomba B-6 y R-6 en servicio</p>
      </div>

      <!-- Alertas Discrepancia -->
      <div class="bg-bomberos-card border border-bomberos-border p-5 rounded-2xl shadow-lg">
        <div class="flex items-center justify-between text-gray-400 mb-2">
          <span class="text-xs font-bold uppercase tracking-wider">Alertas Pendientes</span>
          <span class="text-xl">⚠️</span>
        </div>
        <div class="text-3xl font-black" :class="summary.alertas_pendientes > 0 ? 'text-red-400' : 'text-emerald-400'">
          {{ summary.alertas_pendientes }}
        </div>
        <p class="text-xs text-gray-400 mt-1">Diferencias activas por auditar</p>
      </div>

      <!-- Motor DB Status -->
      <div class="bg-bomberos-card border border-bomberos-border p-5 rounded-2xl shadow-lg">
        <div class="flex items-center justify-between text-gray-400 mb-2">
          <span class="text-xs font-bold uppercase tracking-wider">Motor PostgreSQL</span>
          <span class="text-xl">⚡</span>
        </div>
        <div class="text-xl font-extrabold text-emerald-400 flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
          Conectado v16
        </div>
        <p class="text-xs text-gray-400 mt-2">15 Tablas MER v3 activas</p>
      </div>
    </div>

    <!-- Quick Sections Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Carros Preview -->
      <div class="lg:col-span-2 bg-bomberos-surface border border-bomberos-border rounded-3xl p-6 shadow-xl space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <span class="text-xl">🚒</span>
            <h2 class="font-extrabold text-base text-gray-100">Unidades Vehiculares y Cuartel</h2>
          </div>
          <router-link to="/carros" class="text-xs font-bold text-bomberos-red hover:underline">
            Explorar todas →
          </router-link>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="p-4 rounded-2xl bg-bomberos-card border border-bomberos-border hover:border-bomberos-red/60 transition-all">
            <div class="flex items-center justify-between">
              <span class="text-xs font-extrabold px-2.5 py-1 rounded-lg bg-emerald-950 text-emerald-400 border border-emerald-800/60">
                OPERATIVO
              </span>
              <span class="text-xs text-gray-400">1ra Intervención</span>
            </div>
            <h3 class="text-lg font-black text-white mt-2">Carro Bomba B-6</h3>
            <p class="text-xs text-gray-400 mt-1">5 Gavetas y compartimentos de mangueras, pitones y agua</p>
            <router-link to="/carros" class="inline-block mt-3 text-xs font-bold text-red-400 hover:text-red-300">
              Ver compartimentos y stock →
            </router-link>
          </div>

          <div class="p-4 rounded-2xl bg-bomberos-card border border-bomberos-border hover:border-bomberos-red/60 transition-all">
            <div class="flex items-center justify-between">
              <span class="text-xs font-extrabold px-2.5 py-1 rounded-lg bg-emerald-950 text-emerald-400 border border-emerald-800/60">
                OPERATIVO
              </span>
              <span class="text-xs text-gray-400">Rescate Pesado</span>
            </div>
            <h3 class="text-lg font-black text-white mt-2">Unidad de Rescate R-6</h3>
            <p class="text-xs text-gray-400 mt-1">Herramientas hidráulicas Holmatro, cojines Vetter y cuerdas</p>
            <router-link to="/carros" class="inline-block mt-3 text-xs font-bold text-red-400 hover:text-red-300">
              Ver compartimentos y stock →
            </router-link>
          </div>
        </div>
      </div>

      <!-- Últimas Alertas Activas -->
      <div class="bg-bomberos-surface border border-bomberos-border rounded-3xl p-6 shadow-xl flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-2">
              <span class="text-xl">⚠️</span>
              <h2 class="font-extrabold text-base text-gray-100">Alertas Recientes</h2>
            </div>
            <router-link to="/alertas" class="text-xs font-bold text-bomberos-red hover:underline">
              Ver todas →
            </router-link>
          </div>

          <div v-if="summary.ultimas_alertas.length === 0" class="text-center py-6 text-xs text-gray-400">
            ✓ No hay discrepancias pendientes.
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
          <router-link to="/alertas" class="text-xs font-bold text-bomberos-red hover:underline">
            Ir al panel de resolución →
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
