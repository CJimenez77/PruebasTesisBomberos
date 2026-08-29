<template>
  <aside class="w-64 bg-bomberos-sidebar flex flex-col justify-between shrink-0 shadow-2xl border-r border-red-900/40 text-white min-h-screen">
    <!-- Header / Brand -->
    <div>
      <div class="p-5 flex items-center gap-3 border-b border-red-800/60 bg-bomberos-sidebar-dark/40">
        <div class="w-10 h-10 rounded-xl bg-bomberos-red flex items-center justify-center text-xl shadow-md font-bold">
          🚒
        </div>
        <div>
          <h1 class="font-extrabold text-sm tracking-wide uppercase leading-tight">6ª Compañía</h1>
          <p class="text-xs text-red-200/80 font-medium">Bomberos Chillán Viejo</p>
        </div>
      </div>

      <!-- Navigation Links -->
      <nav class="p-4 space-y-1.5">
        <router-link
          to="/"
          class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-150"
          :class="$route.path === '/' ? 'bg-white/15 text-white font-semibold shadow-inner' : 'text-red-100/80 hover:bg-white/10 hover:text-white'"
        >
          <span class="text-lg">📊</span>
          <span>Panel Principal</span>
        </router-link>

        <router-link
          to="/catalogo"
          class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-150"
          :class="$route.path === '/catalogo' ? 'bg-white/15 text-white font-semibold shadow-inner' : 'text-red-100/80 hover:bg-white/10 hover:text-white'"
        >
          <span class="text-lg">📦</span>
          <span>Catálogo de Bienes</span>
        </router-link>

        <router-link
          to="/carros"
          class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-150"
          :class="$route.path === '/carros' ? 'bg-white/15 text-white font-semibold shadow-inner' : 'text-red-100/80 hover:bg-white/10 hover:text-white'"
        >
          <span class="text-lg">🚒</span>
          <span>Carros y Cuartel</span>
        </router-link>

        <router-link
          to="/inspeccion"
          class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-150"
          :class="$route.path === '/inspeccion' ? 'bg-white/15 text-white font-semibold shadow-inner' : 'text-red-100/80 hover:bg-white/10 hover:text-white'"
        >
          <span class="text-lg">📋</span>
          <span>Inspección Terreno</span>
        </router-link>

        <router-link
          to="/alertas"
          class="flex items-center justify-between px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-150"
          :class="$route.path === '/alertas' ? 'bg-white/15 text-white font-semibold shadow-inner' : 'text-red-100/80 hover:bg-white/10 hover:text-white'"
        >
          <div class="flex items-center gap-3">
            <span class="text-lg">⚠️</span>
            <span>Alertas Mando</span>
          </div>
          <span
            v-if="inspeccionesStore.totalAlertasPendientes > 0"
            class="px-2 py-0.5 rounded-full bg-white text-bomberos-red font-black text-[10px] shadow"
          >
            {{ inspeccionesStore.totalAlertasPendientes }}
          </span>
        </router-link>

        <router-link
          to="/movimientos"
          class="flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-150"
          :class="$route.path === '/movimientos' ? 'bg-white/15 text-white font-semibold shadow-inner' : 'text-red-100/80 hover:bg-white/10 hover:text-white'"
        >
          <span class="text-lg">🔄</span>
          <span>Trazabilidad & Stock</span>
        </router-link>
      </nav>
    </div>

    <!-- User Section / Footer -->
    <div class="p-4 border-t border-red-800/60 bg-bomberos-sidebar-dark/30">
      <div class="flex items-center justify-between gap-2">
        <div class="overflow-hidden">
          <p class="font-bold text-sm truncate">{{ authStore.userName }}</p>
          <span class="inline-block mt-0.5 text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider bg-white/20 text-red-100">
            {{ authStore.userRole }}
          </span>
        </div>
        <button
          @click="handleLogout"
          class="p-2 rounded-lg bg-white/10 hover:bg-white/20 text-red-100 transition-colors"
          title="Cerrar Sesión"
        >
          🚪
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
