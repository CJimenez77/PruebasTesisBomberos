import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import DashboardView from '../views/DashboardView.vue'
import CatalogoView from '../views/CatalogoView.vue'
import CarrosView from '../views/CarrosView.vue'
import InspeccionView from '../views/InspeccionView.vue'
import AlertasView from '../views/AlertasView.vue'
import MovimientosView from '../views/MovimientosView.vue'
import LoginView from '../views/LoginView.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { public: true, title: 'Inicio de Sesión' }
  },
  {
    path: '/',
    name: 'Dashboard',
    component: DashboardView,
    meta: { title: 'Panel Principal' }
  },
  {
    path: '/catalogo',
    name: 'Catalogo',
    component: CatalogoView,
    meta: { title: 'Catálogo de Bienes' }
  },
  {
    path: '/carros',
    name: 'Carros',
    component: CarrosView,
    meta: { title: 'Carros y Ubicaciones' }
  },
  {
    path: '/inspeccion',
    name: 'Inspeccion',
    component: InspeccionView,
    meta: { title: 'Inspección en Terreno' }
  },
  {
    path: '/alertas',
    name: 'Alertas',
    component: AlertasView,
    meta: { title: 'Control de Alertas & Discrepancias' }
  },
  {
    path: '/movimientos',
    name: 'Movimientos',
    component: MovimientosView,
    meta: { title: 'Bitácora de Trazabilidad & Traslados' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation Guard para autenticación
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (!to.meta.public && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
