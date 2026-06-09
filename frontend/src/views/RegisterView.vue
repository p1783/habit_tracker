<template>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl mx-auto">
    <div class="bg-white p-8 rounded-lg shadow-md">
      <h2 class="text-2xl font-bold mb-6">Register</h2>
      <form @submit.prevent="register">
        <div class="mb-4">
          <label class="block text-gray-700 mb-2">Username</label>
          <input v-model="username" type="text" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-indigo-600" required>
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 mb-2">Email</label>
          <input v-model="email" type="email" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-indigo-600" required>
        </div>
        <div class="mb-6">
          <label class="block text-gray-700 mb-2">Password</label>
          <input v-model="password" type="password" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-indigo-600" required>
        </div>
        <button type="submit" class="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition">Register</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const username = ref('')
const email = ref('')
const password = ref('')

const register = async () => {
  try {
    await authStore.register(email.value, username.value, password.value)
    router.push('/login')
  } catch (error) {
    console.error('Registration failed:', error)
  }
}
</script>
