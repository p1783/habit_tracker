<template>
  <div class="max-w-md mx-auto bg-white p-8 rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-6">Register</h2>

    <div v-if="errorMessage" class="bg-red-100 text-red-800 p-3 rounded mb-4">
      {{ errorMessage }}
    </div>

    <div v-if="successMessage" class="bg-green-100 text-green-800 p-3 rounded mb-4">
      {{ successMessage }}
    </div>

    <form @submit.prevent="register">
      <div class="mb-4">
        <label class="block text-gray-700 mb-2">Username</label>
        <input
          v-model="username"
          type="text"
          class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-indigo-600"
          required
        />
      </div>

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
        Register
      </button>
    </form>

    <p class="mt-4 text-center text-gray-600">
      Already have an account?
      <router-link to="/login" class="text-indigo-600 hover:underline">
        Login
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
    successMessage.value = "Account created. You can log in now.";

    setTimeout(() => {
      router.push("/login");
    }, 700);
  } catch (error: any) {
    errorMessage.value =
      error.response?.data?.detail || "Registration failed.";
  }
};
</script>