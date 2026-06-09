<template>
  <div id="app" class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-indigo-600">📅 Habit Tracker</h1>
          <div class="flex gap-4">
            <router-link to="/" class="text-gray-600 hover:text-indigo-600">Home</router-link>
            <router-link to="/habits" class="text-gray-600 hover:text-indigo-600">Habits</router-link>
            <button @click="logout" class="text-gray-600 hover:text-red-600">Logout</button>
          </div>
        </div>
      </div>
    </nav>
    <main class="max-w-7xl mx-auto px-4 py-8">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
</style>
