<template>
  <div class="p-6 space-y-6 max-w-7xl mx-auto">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-black text-white tracking-tight">Catálogo de Bienes e Inventario</h1>
        <p class="text-xs text-gray-400 mt-0.5">Gestión de activos institucionales: Bienes con QR vs Agrupables por lote</p>
      </div>

      <button
        @click="showModal = true"
        class="px-4 py-2.5 rounded-xl bg-bomberos-red hover:bg-bomberos-red-hover text-white text-xs font-bold shadow-lg shadow-red-950/40 transition-all flex items-center gap-2"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
        </svg>
        <span>Registrar Nuevo Bien</span>
      </button>
    </div>

    <!-- Filters & Search Bar -->
    <div class="bg-bomberos-surface border border-bomberos-border rounded-2xl p-4 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
      <!-- Search Input -->
      <div class="relative flex-1">
        <svg class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
        <input
          v-model="catalogoStore.searchQuery"
          type="text"
          placeholder="Buscar por nombre, código QR o descripción técnica..."
          class="w-full bg-bomberos-card border border-bomberos-border rounded-xl pl-10 pr-4 py-2.5 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-bomberos-red transition-all"
        />
      </div>

      <!-- Type Filter Tabs -->
      <div class="flex items-center bg-bomberos-card border border-bomberos-border rounded-xl p-1 shrink-0">
        <button
          @click="catalogoStore.selectedTipo = null"
          class="px-3 py-1.5 rounded-lg text-xs font-bold transition-all"
          :class="catalogoStore.selectedTipo === null ? 'bg-bomberos-red text-white shadow' : 'text-gray-400 hover:text-white'"
        >
          Todos ({{ catalogoStore.items.length }})
        </button>
        <button
          @click="catalogoStore.selectedTipo = 'UNITARIO_ETIQUETABLE'"
          class="px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5"
          :class="catalogoStore.selectedTipo === 'UNITARIO_ETIQUETABLE' ? 'bg-bomberos-red text-white shadow' : 'text-gray-400 hover:text-white'"
        >
          <span>Con QR</span>
        </button>
        <button
          @click="catalogoStore.selectedTipo = 'AGRUPABLE_LOTE'"
          class="px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5"
          :class="catalogoStore.selectedTipo === 'AGRUPABLE_LOTE' ? 'bg-bomberos-red text-white shadow' : 'text-gray-400 hover:text-white'"
        >
          <span>Agrupables / Lote</span>
        </button>
      </div>
    </div>

    <!-- Items Grid -->
    <div v-if="catalogoStore.loading" class="text-center py-16 text-xs text-gray-400 font-medium">
      Cargando catálogo institucional...
    </div>

    <div v-else-if="catalogoStore.filteredItems.length === 0" class="bg-bomberos-surface border border-bomberos-border rounded-3xl p-12 text-center">
      <h3 class="text-base font-bold text-white">No se encontraron bienes</h3>
      <p class="text-xs text-gray-400 mt-1">Intente ajustar los términos de búsqueda o el filtro de categoría.</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <ItemCard
        v-for="item in catalogoStore.filteredItems"
        :key="item.id_item"
        :item="item"
      />
    </div>

    <!-- Modal to Create Item -->
    <ItemModal
      v-if="showModal"
      @close="showModal = false"
      @created="handleItemCreated"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import ItemCard from '../components/ItemCard.vue'
import ItemModal from '../components/ItemModal.vue'
import { useCatalogoStore } from '../stores/catalogo'

const catalogoStore = useCatalogoStore()
const showModal = ref(false)

onMounted(async () => {
  await catalogoStore.fetchCatalogo()
})

const handleItemCreated = async () => {
  showModal.value = false
  await catalogoStore.fetchCatalogo()
}
</script>
