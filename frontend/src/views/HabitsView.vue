<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-8">My Habits</h1>
    
    <div class="bg-white p-6 rounded-lg shadow-md mb-8">
      <h2 class="text-xl font-semibold mb-4">Add New Habit</h2>
      <form @submit.prevent="addHabit" class="space-y-4">
        <input v-model="newHabit.name" type="text" placeholder="Habit name" class="w-full px-4 py-2 border rounded-lg" required>
        <textarea v-model="newHabit.description" placeholder="Description" class="w-full px-4 py-2 border rounded-lg"></textarea>
        <select v-model="newHabit.frequency" class="w-full px-4 py-2 border rounded-lg">
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
        </select>
        <button type="submit" class="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700">Add Habit</button>
      </form>
    </div>

    <div class="space-y-4">
      <div v-for="habit in habits" :key="habit.id" class="bg-white p-6 rounded-lg shadow-md">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="text-xl font-semibold">{{ habit.name }}</h3>
            <p class="text-gray-600">{{ habit.description }}</p>
            <span class="text-sm text-gray-500">{{ habit.frequency }}</span>
          </div>
          <button @click="deleteHabit(habit.id)" class="text-red-600 hover:text-red-800">Delete</button>
        </div>
        <button @click="markComplete(habit.id)" class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700">
          Mark as Complete
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiClient } from '@/services/api'

const habits = ref([])
const newHabit = ref({
  name: '',
  description: '',
  frequency: 'daily'
})

const loadHabits = async () => {
  try {
    const response = await apiClient.get('/api/habits')
    habits.value = response.data
  } catch (error) {
    console.error('Failed to load habits:', error)
  }
}

const addHabit = async () => {
  try {
    await apiClient.post('/api/habits', newHabit.value)
    newHabit.value = { name: '', description: '', frequency: 'daily' }
    loadHabits()
  } catch (error) {
    console.error('Failed to add habit:', error)
  }
}

const deleteHabit = async (id: string) => {
  try {
    await apiClient.delete(`/api/habits/${id}`)
    loadHabits()
  } catch (error) {
    console.error('Failed to delete habit:', error)
  }
}

const markComplete = async (habitId: string) => {
  try {
    const today = new Date().toISOString().split('T')[0]
    await apiClient.post(`/api/habits/${habitId}/completions`, {
      completion_date: today
    })
    loadHabits()
  } catch (error) {
    console.error('Failed to mark complete:', error)
  }
}

onMounted(loadHabits)
</script>
