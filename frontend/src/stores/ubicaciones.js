import { defineStore } from 'pinia'
import apiClient from '../api/client'

export const useUbicacionesStore = defineStore('ubicaciones', {
  state: () => ({
    ubicaciones: [],
    tiposUbicacion: [],
    currentStock: [],
    selectedUbicacion: null,
    loading: false,
    error: null,
  }),
  getters: {
    carrosBomba: (state) => state.ubicaciones.filter(u => u.tipo_nombre === 'CARRO_BOMBA'),
    bodegas: (state) => state.ubicaciones.filter(u => u.tipo_nombre !== 'CARRO_BOMBA' && !u.id_ubicacion_padre),
    subUbicacionesDe: (state) => (parentId) => state.ubicaciones.filter(u => u.id_ubicacion_padre === parentId),
  },
  actions: {
    async fetchUbicaciones() {
      this.loading = true
      try {
        const [ubRes, tiposRes] = await Promise.all([
          apiClient.get('/ubicaciones/'),
          apiClient.get('/ubicaciones/tipos'),
        ])
        this.ubicaciones = ubRes.data
        this.tiposUbicacion = tiposRes.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error cargando ubicaciones'
      } finally {
        this.loading = false
      }
    },
    async fetchStock(idUbicacion) {
      this.loading = true
      try {
        const res = await apiClient.get(`/ubicaciones/${idUbicacion}/stock`)
        this.currentStock = res.data
        this.selectedUbicacion = this.ubicaciones.find(u => u.id_ubicacion === idUbicacion)
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error cargando stock de ubicación'
      } finally {
        this.loading = false
      }
    }
  }
})
