<template>
  <div class="max-w-md mx-auto bg-white p-8 rounded-3xl shadow-lg">
    <h2 class="text-3xl font-bold mb-6 text-gray-900">Rejestracja</h2>

    <div v-if="errorMessage" class="bg-red-100 text-red-800 p-3 rounded-xl mb-4">
      {{ errorMessage }}
    </div>

    <div v-if="successMessage" class="bg-green-100 text-green-800 p-3 rounded-xl mb-4">
      {{ successMessage }}
    </div>

    <form @submit.prevent="register">
      <div class="mb-4">
        <label class="block text-gray-700 mb-2">Nazwa użytkownika</label>
        <input v-model="username" type="text" class="w-full px-4 py-3 border rounded-xl focus:outline-none focus:border-purple-600" required />
      </div>

      <div class="mb-4">
        <label class="block text-gray-700 mb-2">Email</label>
        <input v-model="email" type="email" class="w-full px-4 py-3 border rounded-xl focus:outline-none focus:border-purple-600" required />
      </div>

      <div class="mb-6">
        <label class="block text-gray-700 mb-2">Hasło</label>
        <input v-model="password" type="password" class="w-full px-4 py-3 border rounded-xl focus:outline-none focus:border-purple-600" required />
      </div>

      <button type="submit" class="w-full bg-purple-600 text-white py-3 rounded-xl hover:bg-purple-700 transition">
        Zarejestruj
      </button>
    </form>

    <p class="mt-4 text-center text-gray-600">
      Masz już konto?
      <router-link to="/login" class="text-purple-600 hover:underline">
        Zaloguj się
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

const username = ref("");
const email = ref("");
const password = ref("");
const errorMessage = ref("");
const successMessage = ref("");

const register = async () => {
  errorMessage.value = "";
  successMessage.value = "";

  try {
    await authStore.register(email.value, username.value, password.value);
    successMessage.value = "Konto zostało utworzone. Możesz się zalogować.";

    setTimeout(() => {
      router.push("/login");
    }, 700);
  } catch (error: any) {
    errorMessage.value =
      error.response?.data?.detail || "Rejestracja nie powiodła się.";
  }
};
</script>
