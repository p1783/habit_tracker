import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiClient } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<any>(null)

  const isAuthenticated = computed(() => !!token.value)

  const login = async (email: string, password: string) => {
    const response = await apiClient.post('/api/auth/login', { email, password })
    token.value = response.data.access_token
    localStorage.setItem('token', token.value)
    return response.data
  }

  const register = async (email: string, username: string, password: string) => {
    const response = await apiClient.post('/api/auth/register', { email, username, password })
    return response.data
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout
  }
})
