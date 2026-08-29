<template>
  <div class="bg-bomberos-card border border-bomberos-border hover:border-bomberos-red/60 rounded-2xl p-4 transition-all duration-200 shadow-lg hover:shadow-red-950/20 flex flex-col justify-between group">
    <div>
      <!-- Image & Badges -->
      <div class="relative w-full h-36 bg-bomberos-surface rounded-xl overflow-hidden mb-3 border border-bomberos-border/60 flex items-center justify-center">
        <img
          :src="getItemImage(item.id_categoria)"
          :alt="item.nombre"
          class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300 opacity-90 group-hover:opacity-100"
        />
        
        <!-- QR Badge if applicable -->
        <span
          v-if="item.codigo_qr"
          class="absolute top-2 left-2 bg-bomberos-surface/90 backdrop-blur text-gray-200 text-[11px] font-mono font-bold px-2 py-0.5 rounded-lg border border-bomberos-border flex items-center gap-1 shadow"
        >
          <span>📱</span> {{ item.codigo_qr }}
        </span>
        <span
          v-else
          class="absolute top-2 left-2 bg-amber-950/90 backdrop-blur text-amber-300 text-[11px] font-semibold px-2 py-0.5 rounded-lg border border-amber-800/60 flex items-center gap-1 shadow"
        >
          <span>📦</span> Agrupable
        </span>

        <!-- Status Badge -->
        <span
          class="absolute top-2 right-2 text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-md shadow"
          :class="getStatusClass(item.estado)"
        >
          {{ item.estado }}
        </span>
      </div>

      <!-- Item Info -->
      <div class="mb-2">
        <span class="text-[11px] font-bold text-bomberos-gold uppercase tracking-wider block mb-1">
          {{ item.categoria_nombre }}
        </span>
        <h3 class="font-bold text-base text-gray-100 group-hover:text-red-400 transition-colors leading-snug line-clamp-1">
          {{ item.nombre }}
        </h3>
        <p class="text-xs text-gray-400 line-clamp-2 mt-1 min-h-[32px]">
          {{ item.descripcion || 'Sin observaciones registradas.' }}
        </p>
      </div>
    </div>

    <!-- Stock / Quantity Footer -->
    <div class="pt-3 border-t border-bomberos-border/60 flex items-center justify-between mt-2">
      <div class="text-xs text-gray-400">
        Stock Registrado
      </div>
      <div class="text-sm font-extrabold text-gray-100 bg-bomberos-surface px-3 py-1 rounded-lg border border-bomberos-border">
        {{ item.cantidad }} {{ item.tipo_clasificacion === 'AGRUPABLE_LOTE' ? 'unidades' : 'unidad' }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    required: true
  }
})

const getItemImage = (categoriaId) => {
  if ([2, 3].includes(categoriaId)) return '/items/items_herramientas.png'
  if ([1, 5, 7].includes(categoriaId)) return '/items/items_cuartel.png'
  return '/items/items_cabina.png'
}

const getStatusClass = (estado) => {
  switch (estado?.toUpperCase()) {
    case 'OPERATIVO':
    case 'NUEVO':
      return 'bg-emerald-600 text-white'
    case 'BUENO':
      return 'bg-blue-600 text-white'
    case 'EN_MANTENCION':
    case 'REGULAR':
      return 'bg-amber-600 text-white'
    case 'DANADO':
    case 'MALO':
      return 'bg-red-600 text-white'
    default:
      return 'bg-gray-700 text-gray-200'
  }
}
</script>
