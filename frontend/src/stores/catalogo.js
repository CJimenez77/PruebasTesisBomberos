import { defineStore } from 'pinia'
import apiClient from '../api/client'

export const useCatalogoStore = defineStore('catalogo', {
  state: () => ({
    items: [],
    categorias: [],
    tiposItem: [],
    loading: false,
    error: null,
    searchQuery: '',
    selectedCategoria: null,
    selectedTipoItem: null,
  }),
  getters: {
    filteredItems: (state) => {
      return state.items.filter((item) => {
        const matchesQuery = !state.searchQuery || 
          item.nombre.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
          (item.descripcion && item.descripcion.toLowerCase().includes(state.searchQuery.toLowerCase())) ||
          (item.codigo_qr && item.codigo_qr.toLowerCase().includes(state.searchQuery.toLowerCase()))
        
        const matchesCat = !state.selectedCategoria || item.id_categoria === state.selectedCategoria
        const matchesTipo = !state.selectedTipoItem || item.id_tipo_item === state.selectedTipoItem

        return matchesQuery && matchesCat && matchesTipo
      })
    },
    totalItems: (state) => state.items.length,
    agrupablesCount: (state) => state.items.filter(i => i.tipo_clasificacion === 'AGRUPABLE_LOTE').length,
    qrCount: (state) => state.items.filter(i => i.tipo_clasificacion === 'UNITARIO_ETIQUETABLE').length,
  },
  actions: {
    async fetchCatalogo() {
      this.loading = true
      this.error = null
      try {
        const [itemsRes, catRes, tiposRes] = await Promise.all([
          apiClient.get('/catalogo/items'),
          apiClient.get('/catalogo/categorias'),
          apiClient.get('/catalogo/tipos-item'),
        ])
        this.items = itemsRes.data
        this.categorias = catRes.data
        this.tiposItem = tiposRes.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error cargando catálogo'
      } finally {
        this.loading = false
      }
    },
    async createItem(itemData) {
      this.loading = true
      try {
        const res = await apiClient.post('/catalogo/items', itemData)
        this.items.push(res.data)
        return { success: true, item: res.data }
      } catch (err) {
        return { success: false, error: err.response?.data?.detail || 'Error creando ítem' }
      } finally {
        this.loading = false
      }
    }
  }
})
