<template>
  <div class="min-h-screen flex items-center justify-center bg-bomberos-bg p-4">
    <div class="w-full max-w-xl bg-bomberos-surface border border-bomberos-border rounded-3xl p-8 shadow-2xl space-y-6 relative overflow-hidden">
      <!-- Institutional Top Bar -->
      <div class="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-bomberos-red via-bomberos-red-hover to-bomberos-red"></div>

      <!-- Institutional Logo & Header -->
      <div class="text-center space-y-2">
        <div class="w-16 h-16 rounded-2xl bg-bomberos-red text-white mx-auto flex items-center justify-center shadow-lg">
          <svg class="w-9 h-9" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
          </svg>
        </div>
        <h1 class="text-2xl font-black tracking-tight text-white uppercase">Sexta Compañía</h1>
        <p class="text-xs text-gray-400 font-medium tracking-wide">Cuerpo de Bomberos de Chillán Viejo</p>
        <div class="inline-block px-3 py-1 rounded-full bg-bomberos-card border border-bomberos-border text-[11px] font-semibold text-gray-300">
          Sistema Integrado de Control de Inventario y Trazabilidad
        </div>
      </div>

      <!-- Error Alert -->
      <div v-if="error" class="p-3.5 rounded-xl bg-red-950/80 border border-red-800 text-xs text-red-200 flex items-center gap-2">
        <svg class="w-4 h-4 shrink-0 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span>{{ error }}</span>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1.5">
            Correo Institucional / RUN
          </label>
          <input
            v-model="email"
            type="text"
            required
            placeholder="usuario@bomberoschillanviejo.cl"
            class="w-full bg-bomberos-card border border-bomberos-border focus:border-bomberos-red rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 focus:outline-none transition-all"
          />
        </div>

        <div>
          <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1.5">
            Contraseña
          </label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="••••••••••••"
            class="w-full bg-bomberos-card border border-bomberos-border focus:border-bomberos-red rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 focus:outline-none transition-all"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-bomberos-red hover:bg-bomberos-red-hover text-white font-bold py-3.5 px-4 rounded-xl shadow-lg shadow-red-950/50 transition-all duration-150 disabled:opacity-50 text-sm tracking-wide uppercase flex items-center justify-center gap-2"
        >
          <span v-if="loading">Verificando Credenciales...</span>
          <span v-else>Ingresar al Portal Institucional</span>
        </button>
      </form>

      <!-- Functional Profiles Selector -->
      <div class="pt-4 border-t border-bomberos-border/60 space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-[11px] font-extrabold uppercase tracking-wider text-gray-400">
            Acceso Rápido por Funcionalidad Operativa
          </span>
          <span class="text-[10px] text-gray-500 font-mono">Entorno Staging</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
          <!-- Perfil 1: Resolución de Alertas & Mando -->
          <button
            type="button"
            @click="setQuickProfile('cristian.jimenez2201@alumnos.ubiobio.cl', 'DIRECTOR')"
            class="text-left p-3 rounded-xl bg-bomberos-card border border-bomberos-border hover:border-bomberos-red transition-all group"
          >
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-white group-hover:text-red-400 transition-colors">
                Mando & Resolución de Alertas
              </span>
              <span class="text-[10px] font-extrabold px-1.5 py-0.5 rounded bg-red-950 text-red-400 border border-red-800">
                DIRECTOR
              </span>
            </div>
            <p class="text-[11px] text-gray-400 mt-1 leading-tight">
              Visación y cierre formal de discrepancias patrimoniales y reportes de mando.
            </p>
          </button>

          <!-- Perfil 2: Inspección Terreno Post-Emergencia -->
          <button
            type="button"
            @click="setQuickProfile('matias.aguilera@alumnos.ubiobio.cl', 'CAPITAN')"
            class="text-left p-3 rounded-xl bg-bomberos-card border border-bomberos-border hover:border-bomberos-red transition-all group"
          >
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-white group-hover:text-red-400 transition-colors">
                Inspecciones Post-Emergencia
              </span>
              <span class="text-[10px] font-extrabold px-1.5 py-0.5 rounded bg-red-950 text-red-400 border border-red-800">
                CAPITÁN
              </span>
            </div>
            <p class="text-[11px] text-gray-400 mt-1 leading-tight">
              Recuento en terreno tras retorno de siniestros y auditoría de carros bomba.
            </p>
          </button>

          <!-- Perfil 3: Altas, Bajas & Recepción de Material -->
          <button
            type="button"
            @click="setQuickProfile('teniente1@bomberoschillanviejo.cl', 'TENIENTE')"
            class="text-left p-3 rounded-xl bg-bomberos-card border border-bomberos-border hover:border-bomberos-red transition-all group"
          >
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-white group-hover:text-red-400 transition-colors">
                Altas, Bajas & Recepción
              </span>
              <span class="text-[10px] font-extrabold px-1.5 py-0.5 rounded bg-amber-950 text-amber-400 border border-amber-800">
                TENIENTE
              </span>
            </div>
            <p class="text-[11px] text-gray-400 mt-1 leading-tight">
              Incorporación de compras/donaciones y tramitación de bajas por deterioro.
            </p>
          </button>

          <!-- Perfil 4: Trazabilidad & Movimientos entre Unidades -->
          <button
            type="button"
            @click="setQuickProfile('inventario@bomberoschillanviejo.cl', 'ENCARGADO_INVENTARIO')"
            class="text-left p-3 rounded-xl bg-bomberos-card border border-bomberos-border hover:border-bomberos-red transition-all group"
          >
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-white group-hover:text-red-400 transition-colors">
                Trazabilidad & Traslados
              </span>
              <span class="text-[10px] font-extrabold px-1.5 py-0.5 rounded bg-blue-950 text-blue-400 border border-blue-800">
                ENCARGADO
              </span>
            </div>
            <p class="text-[11px] text-gray-400 mt-1 leading-tight">
              Movimientos de stock entre Bodega Central, Carro B-6 y Unidad R-6.
            </p>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const email = ref('cristian.jimenez2201@alumnos.ubiobio.cl')
const password = ref('bomberos2026_staging')
const loading = ref(false)
const error = ref('')

const authStore = useAuthStore()
const router = useRouter()

const setQuickProfile = (targetEmail, roleName) => {
  email.value = targetEmail
  password.value = 'bomberos2026_staging'
}

const handleSubmit = async () => {
  loading.value = true
  error.value = ''
  try {
    const success = await authStore.login(email.value, password.value)
    if (success) {
      router.push('/')
    } else {
      error.value = authStore.error || 'Error al iniciar sesión. Verifique sus credenciales.'
    }
  } catch (err) {
    error.value = 'No se pudo conectar con el servidor de autenticación.'
  } finally {
    loading.value = false
  }
}
</script>
