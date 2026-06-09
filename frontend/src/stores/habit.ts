import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiClient } from '@/services/api'

export const useHabitStore = defineStore('habit', () => {
  const habits = ref<any[]>([])
  const completions = ref<any[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const activeHabits = computed(() => habits.value.filter(h => h.is_active))
  const inactiveHabits = computed(() => habits.value.filter(h => !h.is_active))

  const loadHabits = async (isActive: boolean | null = null) => {
    loading.value = true
    error.value = null
    try {
      const params = isActive !== null ? { is_active: isActive } : {}
      const response = await apiClient.get('/api/habits', { params })
      habits.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to load habits'
    } finally {
      loading.value = false
    }
  }

  const createHabit = async (habitData: any) => {
    loading.value = true
    error.value = null
    try {
      const response = await apiClient.post('/api/habits', habitData)
      habits.value.push(response.data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to create habit'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateHabit = async (habitId: string, habitData: any) => {
    loading.value = true
    error.value = null
    try {
      const response = await apiClient.put(`/api/habits/${habitId}`, habitData)
      const index = habits.value.findIndex(h => h.id === habitId)
      if (index !== -1) {
        habits.value[index] = response.data
      }
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to update habit'
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteHabit = async (habitId: string) => {
    loading.value = true
    error.value = null
    try {
      await apiClient.delete(`/api/habits/${habitId}`)
      habits.value = habits.value.filter(h => h.id !== habitId)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete habit'
      throw err
    } finally {
      loading.value = false
    }
  }

  const searchHabits = async (query: string) => {
    loading.value = true
    error.value = null
    try {
      const response = await apiClient.get('/api/habits/search', { params: { query } })
      habits.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to search habits'
    } finally {
      loading.value = false
    }
  }

  const markComplete = async (habitId: string, completionDate: string, notes: string = '') => {
    loading.value = true
    error.value = null
    try {
      const response = await apiClient.post(`/api/habits/${habitId}/completions`, {
        completion_date: completionDate,
        notes
      })
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to mark habit as complete'
      throw err
    } finally {
      loading.value = false
    }
  }

  const loadCompletions = async (habitId: string, startDate?: string, endDate?: string) => {
    loading.value = true
    error.value = null
    try {
      const params: any = {}
      if (startDate) params.start_date = startDate
      if (endDate) params.end_date = endDate
      const response = await apiClient.get(`/api/habits/${habitId}/completions`, { params })
      completions.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to load completions'
    } finally {
      loading.value = false
    }
  }

  const deleteCompletion = async (habitId: string, completionId: string) => {
    loading.value = true
    error.value = null
    try {
      await apiClient.delete(`/api/habits/${habitId}/completions/${completionId}`)
      completions.value = completions.value.filter(c => c.id !== completionId)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to delete completion'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    habits,
    completions,
    loading,
    error,
    activeHabits,
    inactiveHabits,
    loadHabits,
    createHabit,
    updateHabit,
    deleteHabit,
    searchHabits,
    markComplete,
    loadCompletions,
    deleteCompletion
  }
})
