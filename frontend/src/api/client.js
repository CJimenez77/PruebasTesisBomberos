import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para inyectar token JWT
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('bomberos_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor para capturar expiración de sesión (401)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      if (window.location.pathname !== '/login') {
        localStorage.removeItem('bomberos_token')
        localStorage.removeItem('bomberos_user')
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient
