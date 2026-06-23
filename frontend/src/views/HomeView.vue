<template>
  <div class="max-w-6xl mx-auto">
    <section class="bg-white rounded-3xl shadow-lg p-8 mb-8 border border-purple-100">
      <p class="text-sm font-semibold text-purple-600 mb-2">Dashboard</p>

      <h1 class="text-4xl font-bold text-gray-900 mb-3">
        Dzień dobry 👋
      </h1>

      <p class="text-gray-600 text-lg mb-6">
        Tutaj możesz szybko sprawdzić dzisiejszy postęp i przejść do zarządzania nawykami.
      </p>

      <router-link
        to="/habits"
        class="inline-block bg-purple-600 text-white px-6 py-3 rounded-2xl hover:bg-purple-700 shadow-md transition hover:scale-[1.02]"
      >
        Przejdź do nawyków
      </router-link>
    </section>

    <section class="grid grid-cols-1 md:grid-cols-4 gap-5 mb-8">
      <div class="bg-white rounded-3xl p-6 shadow border border-purple-100">
        <p class="text-gray-500 text-sm">📋 Wszystkie nawyki</p>
        <p class="text-3xl font-bold text-gray-900">{{ habits.length }}</p>
      </div>

      <div class="bg-white rounded-3xl p-6 shadow border border-purple-100">
        <p class="text-gray-500 text-sm">🔥 Aktywne</p>
        <p class="text-3xl font-bold text-green-600">{{ activeCount }}</p>
      </div>

      <div class="bg-white rounded-3xl p-6 shadow border border-purple-100">
        <p class="text-gray-500 text-sm">✅ Wykonane dzisiaj</p>
        <p class="text-3xl font-bold text-purple-600">{{ completedTodayCount }}</p>
      </div>

      <div class="bg-white rounded-3xl p-6 shadow border border-purple-100">
        <p class="text-gray-500 text-sm">📈 Postęp dnia</p>
        <p class="text-3xl font-bold text-purple-600">{{ todayProgress }}%</p>
      </div>
    </section>

    <section class="bg-white rounded-3xl shadow-lg p-6 border border-purple-100">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-5">
        <div>
          <p class="text-sm font-semibold text-purple-600">Na dziś</p>
          <h2 class="text-2xl font-bold text-gray-900">
            {{ completedTodayCount }} z {{ activeCount }} wykonane
          </h2>
        </div>

        <div class="w-full md:w-72">
          <div class="w-full bg-purple-100 rounded-full h-4 overflow-hidden">
            <div
              class="bg-purple-600 h-4 rounded-full transition-all"
              :style="{ width: todayProgress + '%' }"
            ></div>
          </div>
        </div>
      </div>

      <div v-if="activeHabits.length > 0" class="space-y-3">
        <div
          v-for="habit in activeHabits"
          :key="habit.id"
          class="flex items-center justify-between bg-purple-50 rounded-2xl p-4 border border-purple-100"
        >
          <div>
            <p class="font-semibold text-gray-900">{{ habit.name }}</p>
            <p class="text-sm text-gray-500">
              {{ isCompletedToday(habit.id) ? "Wykonany dzisiaj" : "Do wykonania" }}
            </p>
          </div>

          <span
            :class="isCompletedToday(habit.id) ? 'bg-green-500 text-white' : 'bg-purple-100 text-purple-700'"
            class="px-4 py-2 rounded-xl font-semibold"
          >
            {{ isCompletedToday(habit.id) ? "✓" : "○" }}
          </span>
        </div>
      </div>

      <div v-else class="text-center py-8 text-gray-600">
        🌱 Nie masz jeszcze aktywnych nawyków.
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useHabitStore } from "@/stores/habit";
import { storeToRefs } from "pinia";

const habitStore = useHabitStore();
const { habits, completions } = storeToRefs(habitStore);

const completionMap = ref<Record<string, any[]>>({});
const today = new Date().toISOString().split("T")[0];

const activeHabits = computed(() => habits.value.filter((habit) => habit.is_active));
const activeCount = computed(() => activeHabits.value.length);

const isCompletedToday = (habitId: string) => {
  return (completionMap.value[habitId] || []).some(
    (completion) => completion.completion_date === today
  );
};

const completedTodayCount = computed(() =>
  activeHabits.value.filter((habit) => isCompletedToday(habit.id)).length
);

const todayProgress = computed(() => {
  if (activeCount.value === 0) return 0;
  return Math.round((completedTodayCount.value / activeCount.value) * 100);
});

const loadCompletionMap = async () => {
  for (const habit of habits.value) {
    try {
      await habitStore.loadCompletions(habit.id);
      completionMap.value[habit.id] = [...completions.value];
    } catch {
      completionMap.value[habit.id] = [];
    }
  }
};

onMounted(async () => {
  await habitStore.loadHabits();
  await loadCompletionMap();
});
</script>