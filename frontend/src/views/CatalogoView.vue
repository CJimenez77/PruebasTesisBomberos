<template>
  <div class="p-6 space-y-6 max-w-7xl mx-auto">
    <!-- Header with Search & Add Button -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-black text-white tracking-tight">Catálogo Institucional de Bienes</h1>
        <p class="text-xs text-gray-400 mt-0.5">Control de herramientas, EPP, mobiliario y activos con QR / Conteo</p>
      </div>

      <div class="flex items-center gap-3">
        <button
          @click="showModal = true"
          class="px-4 py-2.5 rounded-xl bg-bomberos-red hover:bg-bomberos-red-hover text-white text-xs font-bold shadow-lg shadow-red-950/40 transition-all flex items-center gap-2"
        >
          <span>➕</span> Registrar Nuevo Bien
        </button>
      </div>
    </div>

    <!-- Filters Bar -->
    <div class="bg-bomberos-surface border border-bomberos-border p-4 rounded-2xl shadow-lg space-y-3">
      <!-- Search Input -->
      <div class="relative">
        <span class="absolute left-3.5 top-3 text-gray-400 text-sm">🔍</span>
        <input
          v-model="catalogoStore.searchQuery"
          type="text"
          placeholder="Buscar por nombre, código QR o descripción..."
          class="w-full bg-bomberos-card border border-bomberos-border rounded-xl pl-10 pr-4 py-2.5 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-bomberos-red"
        />
        <button
          v-if="catalogoStore.searchQuery"
          @click="catalogoStore.searchQuery = ''"
          class="absolute right-3.5 top-2.5 text-gray-400 hover:text-white text-xs font-bold"
        >
          ✕
        </button>
      </div>

      <!-- Classification Filters & Categories -->
      <div class="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-bomberos-border/60">
        <!-- Classification toggle -->
        <div class="flex items-center gap-1.5 bg-bomberos-card p-1 rounded-xl border border-bomberos-border text-xs">
          <button
            @click="catalogoStore.selectedTipoItem = null"
            class="px-3 py-1.5 rounded-lg font-bold transition-all"
            :class="!catalogoStore.selectedTipoItem ? 'bg-bomberos-red text-white' : 'text-gray-400 hover:text-gray-200'"
          >
            Todos ({{ catalogoStore.totalItems }})
          </button>
          <button
            @click="catalogoStore.selectedTipoItem = 2"
            class="px-3 py-1.5 rounded-lg font-bold transition-all flex items-center gap-1"
            :class="catalogoStore.selectedTipoItem === 2 ? 'bg-bomberos-red text-white' : 'text-gray-400 hover:text-gray-200'"
          >
            <span>📱</span> Con QR ({{ catalogoStore.qrCount }})
          </button>
          <button
            @click="catalogoStore.selectedTipoItem = 1"
            class="px-3 py-1.5 rounded-lg font-bold transition-all flex items-center gap-1"
            :class="catalogoStore.selectedTipoItem === 1 ? 'bg-bomberos-red text-white' : 'text-gray-400 hover:text-gray-200'"
          >
            <span>📦</span> Agrupables ({{ catalogoStore.agrupablesCount }})
          </button>
        </div>

        <!-- Categories dropdown -->
        <div class="flex items-center gap-2">
          <span class="text-xs text-gray-400 font-bold hidden sm:inline">Categoría:</span>
          <select
            v-model.number="catalogoStore.selectedCategoria"
            class="bg-bomberos-card border border-bomberos-border rounded-xl px-3 py-1.5 text-xs text-gray-200 focus:outline-none focus:border-bomberos-red"
          >
            <option :value="null">Todas las categorías</option>
            <option v-for="cat in catalogoStore.categorias" :key="cat.id_categoria" :value="cat.id_categoria">
              {{ cat.nombre }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Items Grid -->
    <div v-if="catalogoStore.loading" class="text-center py-16">
      <div class="w-8 h-8 border-3 border-bomberos-red border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
      <p class="text-xs text-gray-400">Cargando catálogo desde PostgreSQL 16...</p>
    </div>

    <div v-else-if="catalogoStore.filteredItems.length === 0" class="bg-bomberos-surface border border-bomberos-border rounded-3xl p-12 text-center">
      <div class="text-4xl mb-3">📦</div>
      <h3 class="text-lg font-bold text-white">No se encontraron bienes</h3>
      <p class="text-xs text-gray-400 mt-1 max-w-sm mx-auto">
        No hay ítems que coincidan con los filtros aplicados. Puedes registrar un nuevo bien usando el botón superior.
      </p>
      <button
        @click="showModal = true"
        class="mt-4 px-4 py-2 bg-bomberos-red hover:bg-bomberos-red-hover text-white text-xs font-bold rounded-xl transition-all"
      >
        Registrar Nuevo Bien
      </button>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
      <ItemCard
        v-for="item in catalogoStore.filteredItems"
        :key="item.id_item"
        :item="item"
      />
    </div>

    <!-- Create Item Modal -->
    <ItemModal
      :isOpen="showModal"
      @close="showModal = false"
      @saved="handleItemSaved"
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

const handleItemSaved = async () => {
  await catalogoStore.fetchCatalogo()
}
</script>
