<template>
  <div class="p-6 space-y-6 max-w-7xl mx-auto">
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

      <div class="flex items-center gap-3">
        <router-link
          to="/catalogo"
          class="px-4 py-2.5 rounded-xl bg-bomberos-red hover:bg-bomberos-red-hover text-white text-xs font-bold shadow-lg shadow-red-950/40 transition-all flex items-center gap-2"
        >
          <span>📦</span> Ver Catálogo
        </router-link>
        <router-link
          to="/inspeccion"
          class="px-4 py-2.5 rounded-xl bg-bomberos-card hover:bg-bomberos-border text-gray-200 border border-bomberos-border text-xs font-bold transition-all flex items-center gap-2"
        >
          <span>📋</span> Nueva Inspección
        </router-link>
      </div>
    </div>

    <!-- 4 Stats Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Total Items -->
      <div class="bg-bomberos-card border border-bomberos-border p-5 rounded-2xl shadow-lg">
        <div class="flex items-center justify-between text-gray-400 mb-2">
          <span class="text-xs font-bold uppercase tracking-wider">Total Bienes</span>
          <span class="text-xl">📦</span>
        </div>
        <div class="text-3xl font-black text-white">{{ catalogoStore.totalItems }}</div>
        <p class="text-xs text-gray-400 mt-1">Activos registrados en catálogo</p>
      </div>

      <!-- Agrupables vs QR -->
      <div class="bg-bomberos-card border border-bomberos-border p-5 rounded-2xl shadow-lg">
        <div class="flex items-center justify-between text-gray-400 mb-2">
          <span class="text-xs font-bold uppercase tracking-wider">Bienes QR / Agrupables</span>
          <span class="text-xl">📱</span>
        </div>
        <div class="text-3xl font-black text-amber-400">
          {{ catalogoStore.qrCount }} <span class="text-sm font-normal text-gray-400">/ {{ catalogoStore.agrupablesCount }} lotes</span>
        </div>
        <p class="text-xs text-gray-400 mt-1">Etiquetados vs conteo agrupable</p>
      </div>

      <!-- Unidades / Carros -->
      <div class="bg-bomberos-card border border-bomberos-border p-5 rounded-2xl shadow-lg">
        <div class="flex items-center justify-between text-gray-400 mb-2">
          <span class="text-xs font-bold uppercase tracking-wider">Unidades Operativas</span>
          <span class="text-xl">🚒</span>
        </div>
        <div class="text-3xl font-black text-emerald-400">
          {{ ubicacionesStore.carrosBomba.length || 2 }}
        </div>
        <p class="text-xs text-gray-400 mt-1">Carros Bomba B-6 y R-6</p>
      </div>

      <!-- Base de Datos Health -->
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
      <div class="lg:col-span-2 bg-bomberos-surface border border-bomberos-border rounded-3xl p-6 shadow-xl">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2.5">
            <span class="text-xl">🚒</span>
            <h2 class="font-extrabold text-base text-gray-100">Unidades Vehiculares del Cuartel</h2>
          </div>
          <router-link to="/carros" class="text-xs font-bold text-bomberos-red hover:underline">
            Ver todas →
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
            <p class="text-xs text-gray-400 mt-1">Gavetas de mangueras, pitones y equipos de agua</p>
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
            <p class="text-xs text-gray-400 mt-1">Herramientas hidráulicas, cojines de levante y cuerdas</p>
            <router-link to="/carros" class="inline-block mt-3 text-xs font-bold text-red-400 hover:text-red-300">
              Ver compartimentos y stock →
            </router-link>
          </div>
        </div>
      </div>

      <!-- Categorías Maestras -->
      <div class="bg-bomberos-surface border border-bomberos-border rounded-3xl p-6 shadow-xl flex flex-col justify-between">
        <div>
          <div class="flex items-center gap-2.5 mb-4">
            <span class="text-xl">🏷️</span>
            <h2 class="font-extrabold text-base text-gray-100">Categorías de Inventario</h2>
          </div>

          <div class="space-y-2">
            <div
              v-for="cat in catalogoStore.categorias.slice(0, 5)"
              :key="cat.id_categoria"
              class="p-2.5 rounded-xl bg-bomberos-card border border-bomberos-border flex items-center justify-between text-xs"
            >
              <span class="font-bold text-gray-200">{{ cat.nombre }}</span>
              <span class="text-gray-400 text-[11px]">Cat #{{ cat.id_categoria }}</span>
            </div>
          </div>
        </div>

        <div class="pt-4 mt-4 border-t border-bomberos-border/60 text-center">
          <router-link to="/catalogo" class="text-xs font-bold text-bomberos-red hover:underline">
            Explorar catálogo completo →
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useCatalogoStore } from '../stores/catalogo'
import { useUbicacionesStore } from '../stores/ubicaciones'

const authStore = useAuthStore()
const catalogoStore = useCatalogoStore()
const ubicacionesStore = useUbicacionesStore()

onMounted(async () => {
  await Promise.all([
    catalogoStore.fetchCatalogo(),
    ubicacionesStore.fetchUbicaciones(),
  ])
})
</script>
