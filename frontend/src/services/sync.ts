import { apiClient } from './api'
import { offlineStorage } from './offline'
import { useHabitStore } from '@/stores/habit'

export class SyncService {
  private syncInProgress = false

  async init(): Promise<void> {
    await offlineStorage.init()
    window.addEventListener('online', () => this.syncData())
  }

  isOnline(): boolean {
    return navigator.onLine
  }

  async syncData(): Promise<void> {
    if (this.syncInProgress || !this.isOnline()) return

    this.syncInProgress = true
    try {
      const habitStore = useHabitStore()
      const syncQueue = await offlineStorage.getSyncQueue()

      for (const item of syncQueue) {
        try {
          switch (item.action) {
            case 'CREATE_HABIT':
              await apiClient.post('/api/habits', item.data)
              break
            case 'UPDATE_HABIT':
              await apiClient.put(`/api/habits/${item.data.id}`, item.data)
              break
            case 'DELETE_HABIT':
              await apiClient.delete(`/api/habits/${item.data.id}`)
              break
            case 'CREATE_COMPLETION':
              await apiClient.post(
                `/api/habits/${item.data.habit_id}/completions`,
                { completion_date: item.data.completion_date, notes: item.data.notes }
              )
              break
          }
        } catch (error) {
          console.error('Sync error for action:', item.action, error)
        }
      }

      await offlineStorage.clearSyncQueue()
      await habitStore.loadHabits()
    } finally {
      this.syncInProgress = false
    }
  }

  async createHabitOffline(habitData: any): Promise<any> {
    if (!this.isOnline()) {
      const habit = { ...habitData, id: `temp_${Date.now()}`, offline: true }
      await offlineStorage.saveHabits([...(await offlineStorage.getHabits()), habit])
      await offlineStorage.addToSyncQueue('CREATE_HABIT', habitData)
      return habit
    } else {
      return apiClient.post('/api/habits', habitData)
    }
  }

  async markCompleteOffline(habitId: string, completionDate: string, notes: string = ''): Promise<any> {
    if (!this.isOnline()) {
      const completion = {
        id: `temp_${Date.now()}`,
        habit_id: habitId,
        completion_date: completionDate,
        notes,
        offline: true
      }
      await offlineStorage.saveCompletions([...(await offlineStorage.getCompletions()), completion])
      await offlineStorage.addToSyncQueue('CREATE_COMPLETION', completion)
      return completion
    } else {
      return apiClient.post(`/api/habits/${habitId}/completions`, {
        completion_date: completionDate,
        notes
      })
    }
  }
}

export const syncService = new SyncService()
