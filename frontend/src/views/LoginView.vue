<template>
  <div class="max-w-md mx-auto bg-white p-8 rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-6">Login</h2>

    <div v-if="errorMessage" class="bg-red-100 text-red-800 p-3 rounded mb-4">
      {{ errorMessage }}
    </div>

    <form @submit.prevent="login">
      <div class="mb-4">
        <label class="block text-gray-700 mb-2">Email</label>
        <input
          v-model="email"
          type="email"
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-indigo-600"
          required
        />
      </div>

      <div class="mb-6">
        <label class="block text-gray-700 mb-2">Password</label>
        <input
          v-model="password"
          type="password"
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-indigo-600"
          required
        />
      </div>

      <button
        type="submit"
        class="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition"
      >
        Login
      </button>
    </form>

    <p class="mt-4 text-center text-gray-600">
      No account?
      <router-link to="/register" class="text-indigo-600 hover:underline">
        Register
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
      error.response?.data?.detail || "Login failed. Check email and password.";
  }
};
</script>