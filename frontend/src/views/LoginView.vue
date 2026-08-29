<template>
  <div class="min-h-screen bg-bomberos-bg flex items-center justify-center p-4">
    <div class="w-full max-w-md bg-bomberos-surface border border-bomberos-border rounded-3xl p-8 shadow-2xl relative overflow-hidden">
      <!-- Top banner accent -->
      <div class="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-bomberos-sidebar via-bomberos-red to-bomberos-gold"></div>

      <!-- Header / Logo -->
      <div class="text-center mb-8">
        <div class="w-16 h-16 rounded-2xl bg-bomberos-red mx-auto flex items-center justify-center text-3xl shadow-xl shadow-red-950/50 mb-3 border border-red-500/30">
          🚒
        </div>
        <h1 class="text-2xl font-extrabold text-white tracking-tight">Sexta Compañía</h1>
        <p class="text-xs text-gray-400 font-medium mt-1">Cuerpo de Bomberos de Chillán Viejo</p>
        <div class="inline-block mt-2 px-3 py-1 rounded-full bg-red-950/60 border border-red-800/40 text-[11px] font-bold text-red-300">
          Módulo de Inventario & Trazabilidad
        </div>
      </div>

      <!-- Error Alert -->
      <div v-if="authStore.error" class="mb-5 p-3 rounded-xl bg-red-950/80 border border-red-800 text-red-200 text-xs flex items-center gap-2">
        <span>⚠️</span> {{ authStore.error }}
      </div>

      <!-- Form -->
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-xs font-bold text-gray-300 uppercase tracking-wider mb-1.5">
            Correo Institucional / RUN
          </label>
          <input
            v-model="email"
            type="text"
            required
            placeholder="cristian.jimenez2201@alumnos.ubiobio.cl"
            class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-4 py-3 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-bomberos-red focus:ring-1 focus:ring-bomberos-red transition-all"
          />
        </div>

        <div>
          <label class="block text-xs font-bold text-gray-300 uppercase tracking-wider mb-1.5">
            Contraseña
          </label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="••••••••••••"
            class="w-full bg-bomberos-card border border-bomberos-border rounded-xl px-4 py-3 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-bomberos-red focus:ring-1 focus:ring-bomberos-red transition-all"
          />
        </div>

        <button
          type="submit"
          :disabled="authStore.loading"
          class="w-full py-3.5 px-4 bg-bomberos-red hover:bg-bomberos-red-hover active:scale-[0.99] text-white font-bold text-sm rounded-xl shadow-xl shadow-red-950/60 transition-all duration-150 flex items-center justify-center gap-2 mt-2 disabled:opacity-50"
        >
          <span v-if="authStore.loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          <span>{{ authStore.loading ? 'Validando Acceso...' : 'Ingresar al Portal' }}</span>
        </button>
      </form>

      <!-- Quick Credentials / Staging Help -->
      <div class="mt-8 pt-5 border-t border-bomberos-border/60">
        <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-2 text-center">
          Credenciales Rápidas de Prueba (Staging)
        </p>
        <div class="grid grid-cols-2 gap-2">
          <button
            type="button"
            @click="setDirector"
            class="p-2 rounded-xl bg-bomberos-card hover:bg-bomberos-border/60 border border-bomberos-border text-[11px] text-gray-300 font-semibold transition-all text-left"
          >
            ⭐ <span class="text-amber-400 font-bold">Director</span> (Cristian)
          </button>
          <button
            type="button"
            @click="setCapitan"
            class="p-2 rounded-xl bg-bomberos-card hover:bg-bomberos-border/60 border border-bomberos-border text-[11px] text-gray-300 font-semibold transition-all text-left"
          >
            🚒 <span class="text-red-400 font-bold">Capitán</span> (Matías)
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

const authStore = useAuthStore()
const router = useRouter()

const email = ref('cristian.jimenez2201@alumnos.ubiobio.cl')
const password = ref('bomberos2026')

const setDirector = () => {
  email.value = 'cristian.jimenez2201@alumnos.ubiobio.cl'
  password.value = 'director2026'
}

const setCapitan = () => {
  email.value = 'matias.aguilera@alumnos.ubiobio.cl'
  password.value = 'capitan2026'
}

const handleLogin = async () => {
  const success = await authStore.login(email.value, password.value)
  if (success) {
    router.push('/')
  }
}
</script>
