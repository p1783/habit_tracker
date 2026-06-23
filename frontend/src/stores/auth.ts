import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { apiClient } from "@/services/api";

export const useAuthStore = defineStore("auth", () => {
  const token = ref<string | null>(localStorage.getItem("token"));
  const user = ref<any>(
    localStorage.getItem("user")
      ? JSON.parse(localStorage.getItem("user") as string)
      : null
  );

  const isAuthenticated = computed(() => !!token.value);

  const login = async (email: string, password: string) => {
    const response = await apiClient.post("/api/auth/login", {
      email,
      password,
    });

    token.value = response.data.access_token;
    user.value = response.data.user || null;

    localStorage.setItem("token", token.value as string);

    if (user.value) {
      localStorage.setItem("user", JSON.stringify(user.value));
    }

    return response.data;
  };

  const register = async (email: string, username: string, password: string) => {
    const response = await apiClient.post("/api/auth/register", {
      email,
      username,
      password,
    });

    return response.data;
  };

  const logout = () => {
    token.value = null;
    user.value = null;
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  };

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
  };
});