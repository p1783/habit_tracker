<template>
  <div id="app" class="min-h-screen bg-gradient-to-br from-purple-100 via-indigo-50 to-white relative overflow-x-hidden">
    <div class="fixed -top-32 -left-32 w-96 h-96 bg-purple-300 rounded-full blur-3xl opacity-30 pointer-events-none"></div>
    <div class="fixed top-20 -right-32 w-96 h-96 bg-indigo-300 rounded-full blur-3xl opacity-25 pointer-events-none"></div>

    <nav class="bg-white/80 shadow-sm border-b border-purple-100 sticky top-0 z-40 backdrop-blur">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <router-link to="/" class="text-2xl font-bold text-purple-700">
            📅 Habit Tracker
          </router-link>

          <div class="flex gap-4 items-center">
            <router-link v-if="isAuthenticated" to="/" class="text-gray-600 hover:text-purple-700">
              Dashboard
            </router-link>

            <router-link v-if="isAuthenticated" to="/habits" class="text-gray-600 hover:text-purple-700">
              Nawyki
            </router-link>

            <router-link v-if="!isAuthenticated" to="/login" class="text-gray-600 hover:text-purple-700">
              Logowanie
            </router-link>

            <router-link v-if="!isAuthenticated" to="/register" class="text-gray-600 hover:text-purple-700">
              Rejestracja
            </router-link>

            <button v-if="isAuthenticated" @click="logout" class="text-gray-600 hover:text-red-600">
              Wyloguj
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="relative z-10 max-w-7xl mx-auto px-4 py-8">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
const router = useRouter();

const isAuthenticated = computed(() => authStore.isAuthenticated);

const logout = () => {
  authStore.logout();
  router.push("/login");
};
</script>