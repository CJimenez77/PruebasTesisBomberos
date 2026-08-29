<template>
  <aside class="w-64 bg-bomberos-sidebar flex flex-col justify-between shrink-0 shadow-2xl border-r border-red-900/40 text-white min-h-screen">
    <!-- Header / Brand -->
    <div>
      <div class="p-5 flex items-center gap-3 border-b border-red-800/60 bg-bomberos-sidebar-dark/40">
        <div class="w-9 h-9 rounded-xl bg-bomberos-red flex items-center justify-center text-white shadow-md">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
          </svg>
        </div>
        <div>
          <h1 class="font-black text-sm tracking-wide uppercase leading-tight">6ª Compañía</h1>
          <p class="text-[11px] text-red-200/80 font-medium">Bomberos Chillán Viejo</p>
        </div>
      </div>

      <!-- Navigation Links -->
      <nav class="p-4 space-y-1.5">
        <!-- Dashboard -->
        <router-link
          to="/"
          class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-150"
          :class="$route.path === '/' ? 'bg-white/15 text-white font-bold shadow-inner' : 'text-red-100/80 hover:bg-white/10 hover:text-white'"
        >
          <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
          </svg>
          <span>Panel Principal</span>
        </router-link>

        <!-- Catalogo -->
        <router-link
          to="/catalogo"
          class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-150"
          :class="$route.path === '/catalogo' ? 'bg-white/15 text-white font-bold shadow-inner' : 'text-red-100/80 hover:bg-white/10 hover:text-white'"
        >
          <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
          </svg>
          <span>Catálogo de Bienes</span>
        </router-link>

        <!-- Carros y Cuartel -->
        <router-link
          to="/carros"
          class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-150"
          :class="$route.path === '/carros' ? 'bg-white/15 text-white font-bold shadow-inner' : 'text-red-100/80 hover:bg-white/10 hover:text-white'"
        >
          <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"></path>
          </svg>
          <span>Carros y Cuartel</span>
        </router-link>

        <!-- Inspeccion -->
        <router-link
          to="/inspeccion"
          class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-150"
          :class="$route.path === '/inspeccion' ? 'bg-white/15 text-white font-bold shadow-inner' : 'text-red-100/80 hover:bg-white/10 hover:text-white'"
        >
          <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
          </svg>
          <span>Inspección Terreno</span>
        </router-link>

        <!-- Alertas Mando -->
        <router-link
          to="/alertas"
          class="flex items-center justify-between px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-150"
          :class="$route.path === '/alertas' ? 'bg-white/15 text-white font-bold shadow-inner' : 'text-red-100/80 hover:bg-white/10 hover:text-white'"
        >
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
            </svg>
            <span>Alertas Mando</span>
          </div>
          <span
            v-if="inspeccionesStore.totalAlertasPendientes > 0"
            class="px-2 py-0.5 rounded-full bg-white text-bomberos-red font-black text-[10px] shadow"
          >
            {{ inspeccionesStore.totalAlertasPendientes }}
          </span>
        </router-link>

        <!-- Trazabilidad & Movimientos -->
        <router-link
          to="/movimientos"
          class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-150"
          :class="$route.path === '/movimientos' ? 'bg-white/15 text-white font-bold shadow-inner' : 'text-red-100/80 hover:bg-white/10 hover:text-white'"
        >
          <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          <span>Trazabilidad & Stock</span>
        </router-link>
      </nav>
    </div>

    <!-- User Section / Footer -->
    <div class="p-4 border-t border-red-800/60 bg-bomberos-sidebar-dark/30">
      <div class="flex items-center justify-between gap-2">
        <div class="overflow-hidden">
          <p class="font-bold text-sm truncate text-white">{{ authStore.userName }}</p>
          <span class="inline-block mt-0.5 text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider bg-white/20 text-red-100">
            {{ authStore.userRole }}
          </span>
        </div>
        <button
          @click="handleLogout"
          class="p-2 rounded-lg bg-white/10 hover:bg-white/20 text-red-100 transition-colors"
          title="Cerrar Sesión"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
          </svg>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useInspeccionesStore } from '../stores/inspecciones'

const authStore = useAuthStore()
const inspeccionesStore = useInspeccionesStore()
const router = useRouter()

onMounted(async () => {
  if (authStore.isAuthenticated) {
    await inspeccionesStore.fetchInspecciones()
  }
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
