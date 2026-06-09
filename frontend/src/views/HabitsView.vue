<template>
  <div class="max-w-6xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold">My Habits</h1>
      <div class="flex gap-4">
        <div v-if="!isOnline" class="bg-yellow-100 text-yellow-800 px-4 py-2 rounded-lg">
          📡 Offline Mode
        </div>
        <button @click="showAddForm = !showAddForm" class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700">
          + Add Habit
        </button>
      </div>
    </div>

    <!-- Add Habit Form -->
    <div v-if="showAddForm" class="bg-white p-6 rounded-lg shadow-md mb-8">
      <h2 class="text-xl font-semibold mb-4">Create New Habit</h2>
      <form @submit.prevent="addHabit" class="space-y-4">
        <div>
          <label class="block text-gray-700 font-medium mb-2">Habit Name *</label>
          <input v-model="newHabit.name" type="text" placeholder="e.g., Morning Exercise" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-indigo-600" required>
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-2">Description</label>
          <textarea v-model="newHabit.description" placeholder="Why is this habit important?" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-indigo-600" rows="3"></textarea>
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-2">Frequency *</label>
          <select v-model="newHabit.frequency" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-indigo-600">
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
          </select>
        </div>
        <div class="flex gap-4">
          <button type="submit" class="flex-1 bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition">Create</button>
          <button type="button" @click="showAddForm = false" class="flex-1 bg-gray-300 text-gray-800 py-2 rounded-lg hover:bg-gray-400">Cancel</button>
        </div>
      </form>
    </div>

    <!-- Search and Filter -->
    <div class="bg-white p-4 rounded-lg shadow-md mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <input v-model="searchQuery" @input="performSearch" type="text" placeholder="Search habits..." class="px-4 py-2 border rounded-lg focus:outline-none focus:border-indigo-600">
        <select v-model="filterStatus" @change="applyFilter" class="px-4 py-2 border rounded-lg focus:outline-none focus:border-indigo-600">
          <option value="">All Habits</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
        <select v-model="sortBy" class="px-4 py-2 border rounded-lg focus:outline-none focus:border-indigo-600">
          <option value="name">Sort by Name</option>
          <option value="created">Sort by Created</option>
        </select>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="bg-red-100 text-red-800 p-4 rounded-lg mb-6">
      {{ error }}
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <div class="inline-block animate-spin">
        <div class="text-indigo-600 text-4xl">⏳</div>
      </div>
      <p class="mt-4 text-gray-600">Loading habits...</p>
    </div>

    <!-- Habits Grid -->
    <div v-else-if="filteredHabits.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="habit in filteredHabits" :key="habit.id" class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h3 class="text-xl font-semibold">{{ habit.name }}</h3>
            <span :class="['text-xs px-2 py-1 rounded mt-2 inline-block', habit.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800']">
              {{ habit.is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
          <button @click="toggleEditForm(habit)" class="text-blue-600 hover:text-blue-800">✏️</button>
        </div>
        
        <p v-if="habit.description" class="text-gray-600 text-sm mb-4">{{ habit.description }}</p>
        <p class="text-gray-500 text-xs mb-4">{{ habit.frequency }} • Created: {{ formatDate(habit.created_at) }}</p>
        
        <!-- Edit Form -->
        <div v-if="editingId === habit.id" class="mb-4 p-4 bg-gray-50 rounded-lg">
          <input v-model="editingHabit.name" type="text" class="w-full px-3 py-2 border rounded mb-2">
          <textarea v-model="editingHabit.description" class="w-full px-3 py-2 border rounded mb-2" rows="2"></textarea>
          <div class="flex gap-2">
            <button @click="saveHabitEdit(habit.id)" class="flex-1 bg-green-600 text-white px-3 py-2 rounded text-sm">Save</button>
            <button @click="cancelEdit" class="flex-1 bg-gray-400 text-white px-3 py-2 rounded text-sm">Cancel</button>
          </div>
        </div>

        <!-- Action Buttons -->
        <div v-else class="flex gap-2">
          <button @click="markComplete(habit.id)" class="flex-1 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition text-sm">
            ✓ Complete Today
          </button>
          <button @click="toggleActive(habit.id, habit.is_active)" :class="['flex-1 px-3 py-2 rounded-lg text-sm transition', habit.is_active ? 'bg-yellow-500 text-white hover:bg-yellow-600' : 'bg-blue-600 text-white hover:bg-blue-700']">
            {{ habit.is_active ? '⊘ Deactivate' : '✓ Activate' }}
          </button>
          <button @click="viewHistory(habit)" class="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition text-sm">
            📊 History
          </button>
          <button @click="deleteHabit(habit.id)" class="flex-1 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition text-sm">
            🗑️
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <p class="text-gray-600 text-lg mb-4">No habits yet. Start building better habits today!</p>
      <button @click="showAddForm = true" class="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700">
        Create Your First Habit
      </button>
    </div>

    <!-- History Modal -->
    <div v-if="showHistoryModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-8 rounded-lg max-w-md w-full">
        <h2 class="text-2xl font-bold mb-4">{{ selectedHabitForHistory?.name }} - History</h2>
        
        <div class="mb-4">
          <label class="block text-gray-700 mb-2">Filter by date range:</label>
          <input v-model="historyStartDate" type="date" class="w-full px-4 py-2 border rounded mb-2">
          <input v-model="historyEndDate" type="date" class="w-full px-4 py-2 border rounded">
          <button @click="loadHistory" class="w-full mt-2 bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700">Apply Filter</button>
        </div>

        <div v-if="completionHistory.length > 0" class="space-y-2 max-h-96 overflow-y-auto">
          <div v-for="completion in completionHistory" :key="completion.id" class="border-l-4 border-green-600 pl-4 py-2">
            <p class="font-semibold">{{ formatDate(completion.completion_date) }}</p>
            <p v-if="completion.notes" class="text-sm text-gray-600">{{ completion.notes }}</p>
            <button @click="deleteCompletion(selectedHabitForHistory?.id, completion.id)" class="text-red-600 text-sm hover:text-red-800">Remove</button>
          </div>
        </div>
        <div v-else class="text-gray-600 text-center py-4">
          No completions recorded
        </div>

        <button @click="showHistoryModal = false" class="w-full mt-4 bg-gray-400 text-white py-2 rounded hover:bg-gray-500">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useHabitStore } from '@/stores/habit'
import { syncService } from '@/services/sync'

const habitStore = useHabitStore()
const showAddForm = ref(false)
const showHistoryModal = ref(false)
const editingId = ref<string | null>(null)
const selectedHabitForHistory = ref<any>(null)
const isOnline = ref(true)
const searchQuery = ref('')
const filterStatus = ref('')
const sortBy = ref('name')
const historyStartDate = ref('')
const historyEndDate = ref('')

const newHabit = ref({
  name: '',
  description: '',
  frequency: 'daily'
})

const editingHabit = ref({
  name: '',
  description: ''
})

const { habits, completions, loading, error } = habitStore

const filteredHabits = computed(() => {
  let result = [...habits.value]
  
  if (searchQuery.value) {
    result = result.filter(h => h.name.toLowerCase().includes(searchQuery.value.toLowerCase()))
  }
  
  if (sortBy.value === 'name') {
    result.sort((a, b) => a.name.localeCompare(b.name))
  }
  
  return result
})

const completionHistory = computed(() => completions.value.sort((a, b) => 
  new Date(b.completion_date).getTime() - new Date(a.completion_date).getTime()
))

const formatDate = (dateStr: string): string => {
  return new Date(dateStr).toLocaleDateString('pl-PL', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const addHabit = async () => {
  try {
    await habitStore.createHabit(newHabit.value)
    newHabit.value = { name: '', description: '', frequency: 'daily' }
    showAddForm.value = false
  } catch (err) {
    console.error('Error adding habit:', err)
  }
}

const toggleEditForm = (habit: any) => {
  editingId.value = habit.id
  editingHabit.value = {
    name: habit.name,
    description: habit.description
  }
}

const cancelEdit = () => {
  editingId.value = null
}

const saveHabitEdit = async (habitId: string) => {
  try {
    await habitStore.updateHabit(habitId, editingHabit.value)
    editingId.value = null
  } catch (err) {
    console.error('Error updating habit:', err)
  }
}

const toggleActive = async (habitId: string, currentStatus: boolean) => {
  try {
    await habitStore.updateHabit(habitId, { is_active: !currentStatus })
  } catch (err) {
    console.error('Error toggling habit:', err)
  }
}

const deleteHabit = async (habitId: string) => {
  if (confirm('Are you sure you want to delete this habit?')) {
    try {
      await habitStore.deleteHabit(habitId)
    } catch (err) {
      console.error('Error deleting habit:', err)
    }
  }
}

const markComplete = async (habitId: string) => {
  try {
    const today = new Date().toISOString().split('T')[0]
    const notes = prompt('Add notes (optional):', '')
    await habitStore.markComplete(habitId, today, notes || '')
    await habitStore.loadHabits()
  } catch (err: any) {
    if (err.response?.data?.detail?.includes('already completed')) {
      alert('This habit is already marked as complete for today!')
    } else {
      console.error('Error marking complete:', err)
    }
  }
}

const performSearch = () => {
  if (searchQuery.value) {
    habitStore.searchHabits(searchQuery.value)
  } else {
    habitStore.loadHabits()
  }
}

const applyFilter = () => {
  if (filterStatus.value === 'active') {
    habitStore.loadHabits(true)
  } else if (filterStatus.value === 'inactive') {
    habitStore.loadHabits(false)
  } else {
    habitStore.loadHabits()
  }
}

const viewHistory = async (habit: any) => {
  selectedHabitForHistory.value = habit
  showHistoryModal.value = true
  await habitStore.loadCompletions(habit.id)
}

const loadHistory = async () => {
  if (selectedHabitForHistory.value) {
    await habitStore.loadCompletions(
      selectedHabitForHistory.value.id,
      historyStartDate.value,
      historyEndDate.value
    )
  }
}

const deleteCompletion = async (habitId: string, completionId: string) => {
  if (confirm('Remove this completion?')) {
    try {
      await habitStore.deleteCompletion(habitId, completionId)
    } catch (err) {
      console.error('Error deleting completion:', err)
    }
  }
}

const checkOnlineStatus = () => {
  isOnline.value = navigator.onLine
}

onMounted(async () => {
  await syncService.init()
  await habitStore.loadHabits()
  window.addEventListener('online', checkOnlineStatus)
  window.addEventListener('offline', checkOnlineStatus)
})
</script>
