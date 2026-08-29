import { defineStore } from 'pinia'
import apiClient from '../api/client'

export const useInspeccionesStore = defineStore('inspecciones', {
  state: () => ({
    inspecciones: [],
    alertas: [],
    estadosAlerta: [],
    tiposInspeccion: [],
    loading: false,
    error: null,
  }),
  getters: {
    alertasPendientes: (state) => state.alertas.filter(a => !a.resuelta),
    alertasResueltas: (state) => state.alertas.filter(a => a.resuelta),
    totalAlertasPendientes: (state) => state.alertas.filter(a => !a.resuelta).length,
  },
  actions: {
    async fetchInspecciones() {
      this.loading = true
      try {
        const [inspRes, alertRes, estRes, tiposRes] = await Promise.all([
          apiClient.get('/inspecciones/'),
          apiClient.get('/inspecciones/alertas'),
          apiClient.get('/inspecciones/estados-alerta'),
          apiClient.get('/inspecciones/tipos'),
        ])
        this.inspecciones = inspRes.data
        this.alertas = alertRes.data
        this.estadosAlerta = estRes.data
        this.tiposInspeccion = tiposRes.data
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error cargando inspecciones'
      } finally {
        this.loading = false
      }
    },
    async createInspeccion(payload) {
      this.loading = true
      try {
        const res = await apiClient.post('/inspecciones/', payload)
        this.inspecciones.unshift(res.data)
        // Refrescar alertas
        const alertRes = await apiClient.get('/inspecciones/alertas')
        this.alertas = alertRes.data
        return { success: true, inspeccion: res.data }
      } catch (err) {
        return { success: false, error: err.response?.data?.detail || 'Error registrando inspección' }
      } finally {
        this.loading = false
      }
    },
    async resolverAlerta(idAlerta, resolucionPayload) {
      this.loading = true
      try {
        const res = await apiClient.post(`/inspecciones/alertas/${idAlerta}/resolver`, resolucionPayload)
        const idx = this.alertas.findIndex(a => a.id_alerta === idAlerta)
        if (idx !== -1) {
          this.alertas[idx] = res.data
        }
        return { success: true, alerta: res.data }
      } catch (err) {
        return { success: false, error: err.response?.data?.detail || 'Error resolviendo alerta' }
      } finally {
        this.loading = false
      }
    }
  }
})
