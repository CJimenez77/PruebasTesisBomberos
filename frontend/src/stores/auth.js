import { defineStore } from 'pinia'
import apiClient from '../api/client'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('bomberos_token') || null,
    user: JSON.parse(localStorage.getItem('bomberos_user') || 'null'),
    loading: false,
    error: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.role || 'BOMBERO_VOLUNTARIO',
    userName: (state) => state.user?.user_name || 'Voluntario',
  },
  actions: {
    async login(username, password) {
      this.loading = true
      this.error = null
      try {
        const formData = new URLSearchParams()
        formData.append('username', username)
        formData.append('password', password)

        const response = await apiClient.post('/auth/login', formData, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        })

        const data = response.data
        this.token = data.access_token
        this.user = {
          user_id: data.user_id,
          user_name: data.user_name,
          role: data.role,
          email: username,
        }

        localStorage.setItem('bomberos_token', this.token)
        localStorage.setItem('bomberos_user', JSON.stringify(this.user))
        return true
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error al iniciar sesión'
        return false
      } finally {
        this.loading = false
      }
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('bomberos_token')
      localStorage.removeItem('bomberos_user')
    }
  }
})
