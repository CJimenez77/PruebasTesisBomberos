<template>
  <header class="h-16 bg-bomberos-surface/90 backdrop-blur border-b border-bomberos-border px-6 flex items-center justify-between shrink-0 sticky top-0 z-30">
    <div class="flex items-center gap-3">
      <h2 class="font-bold text-lg text-gray-100 tracking-tight">{{ title }}</h2>
      <span class="text-xs px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800/60 font-medium flex items-center gap-1.5">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
        Staging Conectado (PostgreSQL 16)
      </span>
    </div>

    <div class="flex items-center gap-4">
      <div class="text-right hidden sm:block">
        <p class="text-xs text-gray-400">Ambiente UBB Titulación</p>
        <p class="text-xs font-semibold text-gray-200">Cristian Jiménez & Matías Aguilera</p>
      </div>
    </div>
  </header>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: 'Panel de Control'
  }
})
</script>
