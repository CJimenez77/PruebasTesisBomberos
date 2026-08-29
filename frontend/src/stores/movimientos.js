import { defineStore } from 'pinia'
import apiClient from '../api/client'

export const useMovimientosStore = defineStore('movimientos', {
  state: () => ({
    movimientos: [],
    tiposMovimiento: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchMovimientos(filters = {}) {
      this.loading = true
      try {
        const [movsRes, tiposRes] = await Promise.all([
          apiClient.get('/movimientos/', { params: filters }),
          apiClient.get('/movimientos/tipos'),
        ])
        this.movimientos = movsRes.data
        this.tiposMovimiento = tiposRes.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error cargando movimientos'
      } finally {
        this.loading = false
      }
    },
    async createMovimiento(movData) {
      this.loading = true
      try {
        const res = await apiClient.post('/movimientos/', movData)
        this.movimientos.unshift(res.data)
        return { success: true, movimiento: res.data }
      } catch (err) {
        return { success: false, error: err.response?.data?.detail || 'Error registrando movimiento' }
      } finally {
        this.loading = false
      }
    }
  }
})
