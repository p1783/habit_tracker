<template>
  <div class="app">
    <header v-if="isAuthenticated" class="header">
      <div class="header-content">
        <h1>Habit Tracker</h1>
        <nav class="header-nav">
          <router-link to="/">Dashboard</router-link>
          <a href="#" @click.prevent="logout">Logout</a>
        </nav>
      </div>
    </header>
    <router-view />
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from './services'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const isAuthenticated = ref(authService.isAuthenticated())

    const logout = () => {
      authService.logout()
      isAuthenticated.value = false
      router.push('/login')
    }

    return {
      isAuthenticated,
      logout,
    }
  },
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  background-color: #f5f5f5;
}
</style>
