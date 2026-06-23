<template>
  <div class="max-w-md mx-auto bg-white p-8 rounded-3xl shadow-lg">
    <h2 class="text-3xl font-bold mb-6 text-gray-900">Logowanie</h2>

    <div v-if="errorMessage" class="bg-red-100 text-red-800 p-3 rounded-xl mb-4">
      {{ errorMessage }}
    </div>

    <form @submit.prevent="login">
      <div class="mb-4">
        <label class="block text-gray-700 mb-2">Email</label>
        <input
          v-model="email"
          type="email"
          class="w-full px-4 py-3 border rounded-xl focus:outline-none focus:border-purple-600"
          required
        />
      </div>

      <div class="mb-6">
        <label class="block text-gray-700 mb-2">Hasło</label>
        <input
          v-model="password"
          type="password"
          class="w-full px-4 py-3 border rounded-xl focus:outline-none focus:border-purple-600"
          required
        />
      </div>

      <button
        type="submit"
        class="w-full bg-purple-600 text-white py-3 rounded-xl hover:bg-purple-700 transition"
      >
        Zaloguj
      </button>
    </form>

    <p class="mt-4 text-center text-gray-600">
      Nie masz konta?
      <router-link to="/register" class="text-purple-600 hover:underline">
        Zarejestruj się
      </router-link>
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const email = ref("");
const password = ref("");
const errorMessage = ref("");

const login = async () => {
  errorMessage.value = "";

  try {
    await authStore.login(email.value, password.value);
    router.push("/habits");
  } catch (error: any) {
    errorMessage.value =
      error.response?.data?.detail || "Logowanie nie powiodło się.";
  }
};
</script>