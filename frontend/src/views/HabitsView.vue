<template>
  <div class="max-w-6xl mx-auto">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold">My Habits</h1>

      <button
        @click="showAddForm = !showAddForm"
        class="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700"
      >
        + Add Habit
      </button>
    </div>

    <div v-if="showAddForm" class="bg-white p-6 rounded-lg shadow-md mb-8">
      <h2 class="text-xl font-semibold mb-4">Create New Habit</h2>

      <form @submit.prevent="addHabit" class="space-y-4">
        <div>
          <label class="block text-gray-700 font-medium mb-2">Habit Name</label>
          <input
            v-model="newHabit.name"
            type="text"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-indigo-600"
            required
          />
        </div>

        <div>
          <label class="block text-gray-700 font-medium mb-2">Description</label>
          <textarea
            v-model="newHabit.description"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-indigo-600"
            rows="3"
          ></textarea>
        </div>

        <div class="flex gap-4">
          <button
            type="submit"
            class="flex-1 bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700"
          >
            Create
          </button>

          <button
            type="button"
            @click="showAddForm = false"
            class="flex-1 bg-gray-300 text-gray-800 py-2 rounded-lg hover:bg-gray-400"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>

    <div class="bg-white p-4 rounded-lg shadow-md mb-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input
          v-model="searchQuery"
          @input="performSearch"
          type="text"
          placeholder="Search habits..."
          class="px-4 py-2 border rounded-lg focus:outline-none focus:border-indigo-600"
        />

        <select
          v-model="filterStatus"
          @change="applyFilter"
          class="px-4 py-2 border rounded-lg focus:outline-none focus:border-indigo-600"
        >
          <option value="">All Habits</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
      </div>
    </div>

    <div v-if="error" class="bg-red-100 text-red-800 p-4 rounded-lg mb-6">
      {{ error }}
    </div>

    <div v-if="loading" class="text-center py-8">
      Loading habits...
    </div>

    <div
      v-else-if="habits.length > 0"
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      <div
        v-for="habit in habits"
        :key="habit.id"
        class="bg-white p-6 rounded-lg shadow-md"
      >
        <h3 class="text-xl font-semibold mb-2">{{ habit.name }}</h3>

        <p v-if="habit.description" class="text-gray-600 text-sm mb-4">
          {{ habit.description }}
        </p>

        <p class="mb-4">
          <span
            :class="habit.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
            class="text-xs px-2 py-1 rounded"
          >
            {{ habit.is_active ? "Active" : "Inactive" }}
          </span>
        </p>

        <div class="flex flex-col gap-2">
          <button
            @click="markComplete(habit.id)"
            class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
          >
            Complete Today
          </button>

          <button
            @click="toggleActive(habit)"
            class="bg-yellow-500 text-white px-4 py-2 rounded-lg hover:bg-yellow-600"
          >
            {{ habit.is_active ? "Deactivate" : "Activate" }}
          </button>

          <button
            @click="viewHistory(habit)"
            class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            History
          </button>

          <button
            @click="deleteHabit(habit.id)"
            class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
          >
            Delete
          </button>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12">
      <p class="text-gray-600 text-lg mb-4">No habits yet.</p>
      <button
        @click="showAddForm = true"
        class="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700"
      >
        Create Your First Habit
      </button>
    </div>

    <div
      v-if="showHistoryModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white p-8 rounded-lg max-w-md w-full">
        <h2 class="text-2xl font-bold mb-4">
          {{ selectedHabit?.name }} - History
        </h2>

        <div class="mb-4">
          <input
            v-model="historyStartDate"
            type="date"
            class="w-full px-4 py-2 border rounded mb-2"
          />

          <input
            v-model="historyEndDate"
            type="date"
            class="w-full px-4 py-2 border rounded mb-2"
          />

          <button
            @click="loadHistory"
            class="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700"
          >
            Apply Filter
          </button>
        </div>

        <div v-if="completions.length > 0" class="space-y-2 max-h-96 overflow-y-auto">
          <div
            v-for="completion in completions"
            :key="completion.id"
            class="border-l-4 border-green-600 pl-4 py-2"
          >
            <p class="font-semibold">{{ completion.completion_date }}</p>
            <p v-if="completion.notes" class="text-sm text-gray-600">
              {{ completion.notes }}
            </p>
          </div>
        </div>

        <div v-else class="text-gray-600 text-center py-4">
          No completions recorded.
        </div>

        <button
          @click="showHistoryModal = false"
          class="w-full mt-4 bg-gray-400 text-white py-2 rounded hover:bg-gray-500"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { storeToRefs } from "pinia";
import { useHabitStore } from "@/stores/habit";

const habitStore = useHabitStore();
const { habits, completions, loading, error } = storeToRefs(habitStore);

const showAddForm = ref(false);
const showHistoryModal = ref(false);
const selectedHabit = ref<any>(null);

const searchQuery = ref("");
const filterStatus = ref("");
const historyStartDate = ref("");
const historyEndDate = ref("");

const newHabit = ref({
  name: "",
  description: "",
});

const addHabit = async () => {
  await habitStore.createHabit(newHabit.value);
  newHabit.value = { name: "", description: "" };
  showAddForm.value = false;
};

const markComplete = async (habitId: string) => {
  const today = new Date().toISOString().split("T")[0];
  const notes = prompt("Notes optional:", "") || "";

  try {
    await habitStore.markComplete(habitId, today, notes);
    alert("Habit completed.");
  } catch (error: any) {
    alert(error.response?.data?.detail || "Could not complete habit.");
  }
};

const toggleActive = async (habit: any) => {
  await habitStore.updateHabit(habit.id, {
    is_active: !habit.is_active,
  });
};

const deleteHabit = async (habitId: string) => {
  if (confirm("Delete this habit?")) {
    await habitStore.deleteHabit(habitId);
  }
};

const performSearch = async () => {
  if (searchQuery.value.trim()) {
    await habitStore.searchHabits(searchQuery.value);
  } else {
    await habitStore.loadHabits();
  }
};

const applyFilter = async () => {
  if (filterStatus.value === "active") {
    await habitStore.loadHabits(true);
  } else if (filterStatus.value === "inactive") {
    await habitStore.loadHabits(false);
  } else {
    await habitStore.loadHabits();
  }
};

const viewHistory = async (habit: any) => {
  selectedHabit.value = habit;
  showHistoryModal.value = true;
  await habitStore.loadCompletions(habit.id);
};

const loadHistory = async () => {
  if (!selectedHabit.value) return;

  await habitStore.loadCompletions(
    selectedHabit.value.id,
    historyStartDate.value,
    historyEndDate.value
  );
};

onMounted(async () => {
  await habitStore.loadHabits();
});
</script>