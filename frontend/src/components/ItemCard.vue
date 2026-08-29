<template>
  <div class="bg-bomberos-surface border border-bomberos-border hover:border-gray-500 rounded-3xl p-5 shadow-xl transition-all duration-200 flex flex-col justify-between group">
    <div class="space-y-3">
      <!-- Header: Type & Status Badges -->
      <div class="flex items-center justify-between gap-2">
        <span
          class="text-[10px] font-extrabold px-2.5 py-1 rounded-lg uppercase tracking-wider border"
          :class="isUnitario ? 'bg-red-950 text-red-400 border-red-800/80' : 'bg-blue-950 text-blue-400 border-blue-800/80'"
        >
          {{ isUnitario ? 'Unitario con QR' : 'Agrupable / Lote' }}
        </span>

        <span
          class="text-[10px] font-extrabold px-2 py-0.5 rounded-md uppercase"
          :class="item.estado === 'OPERATIVO' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-amber-950 text-amber-400 border border-amber-800'"
        >
          {{ item.estado }}
        </span>
      </div>

      <!-- Item Info -->
      <div>
        <h3 class="font-extrabold text-base text-white group-hover:text-red-400 transition-colors">
          {{ item.nombre }}
        </h3>
        <p class="text-xs text-gray-400 mt-1 line-clamp-2 leading-relaxed">
          {{ item.descripcion || 'Sin descripción técnica registrada.' }}
        </p>
      </div>

      <!-- Details List -->
      <div class="space-y-1.5 pt-2 border-t border-bomberos-border/60 text-xs">
        <div class="flex items-center justify-between text-gray-400">
          <span class="font-medium">Categoría:</span>
          <span class="font-semibold text-gray-200">{{ item.categoria_nombre }}</span>
        </div>

        <div v-if="item.codigo_qr" class="flex items-center justify-between text-gray-400">
          <span class="font-medium">Código QR:</span>
          <code class="px-2 py-0.5 rounded bg-bomberos-card border border-bomberos-border text-red-300 font-mono text-[11px]">
            {{ item.codigo_qr }}
          </code>
        </div>

        <div v-if="item.fecha_vencimiento" class="flex items-center justify-between text-gray-400">
          <span class="font-medium">Vencimiento:</span>
          <span class="font-semibold text-amber-300">{{ item.fecha_vencimiento }}</span>
        </div>
      </div>
    </div>

    <!-- Stock Quantity Footer -->
    <div class="mt-4 pt-3 border-t border-bomberos-border/60 flex items-center justify-between">
      <span class="text-xs text-gray-400 font-medium">Existencia Cuartel:</span>
      <div class="flex items-baseline gap-1">
        <span class="text-xl font-black text-white">{{ item.cantidad }}</span>
        <span class="text-[11px] text-gray-400 uppercase font-semibold">unidades</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
})

const isUnitario = computed(() => {
  return props.item.tipo_clasificacion === 'UNITARIO_ETIQUETABLE' || !!props.item.codigo_qr
})
</script>
