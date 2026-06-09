import { createRouter, createWebHistory } from 'vue-router'
import { authService } from '../services'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import CreateHabit from '../views/CreateHabit.vue'
import EditHabit from '../views/EditHabit.vue'
import HabitHistory from '../views/HabitHistory.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true },
  },
  {
    path: '/habits/create',
    name: 'CreateHabit',
    component: CreateHabit,
    meta: { requiresAuth: true },
  },
  {
    path: '/habits/:id/edit',
    name: 'EditHabit',
    component: EditHabit,
    meta: { requiresAuth: true },
  },
  {
    path: '/habits/:id/history',
    name: 'HabitHistory',
    component: HabitHistory,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const isAuthenticated = authService.isAuthenticated()

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
