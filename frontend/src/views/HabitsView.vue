<template>
  <div class="max-w-7xl mx-auto">
    <div class="mb-8">
      <p class="text-sm font-semibold text-purple-600 mb-2">Panel zarządzania nawykami</p>

      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 class="text-4xl font-bold text-gray-900">Moje nawyki</h1>
          <p class="text-gray-600 mt-2">
            Dodawaj nawyki, oznaczaj wykonanie w wybranych dniach i analizuj historię.
          </p>
        </div>

        <button
          @click="showAddForm = !showAddForm"
          class="bg-purple-600 text-white px-6 py-3 rounded-xl hover:bg-purple-700 shadow-md"
        >
          + Dodaj nawyk
        </button>
      </div>
    </div>

    <div class="bg-white rounded-3xl shadow-lg p-6 mb-8 border border-purple-100">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-5">
        <div>
          <p class="text-sm font-semibold text-purple-600">Dzisiejsze zadania</p>
          <h2 class="text-2xl font-bold text-gray-900">
            {{ completedTodayCount }} z {{ activeCount }} wykonane
          </h2>
        </div>

        <div class="w-full md:w-64 bg-purple-100 rounded-full h-4 overflow-hidden">
          <div
            class="bg-purple-600 h-4 rounded-full transition-all"
            :style="{ width: todayProgress + '%' }"
          ></div>
        </div>
      </div>

      <div v-if="activeHabits.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        <div
          v-for="habit in activeHabits"
          :key="habit.id"
          class="flex items-center justify-between bg-purple-50 rounded-2xl p-4"
        >
          <div>
            <p class="font-semibold text-gray-900">{{ habit.name }}</p>
            <p class="text-sm text-gray-500">
              {{ isCompletedToday(habit.id) ? "Wykonany dzisiaj" : "Do wykonania" }}
            </p>
          </div>

          <button
            @click="quickCompleteToday(habit.id)"
            :disabled="isCompletedToday(habit.id)"
            :class="isCompletedToday(habit.id) ? 'bg-green-500' : 'bg-purple-600 hover:bg-purple-700'"
            class="text-white px-4 py-2 rounded-xl disabled:opacity-80"
          >
            {{ isCompletedToday(habit.id) ? "✓" : "Oznacz" }}
          </button>
        </div>
      </div>

      <p v-else class="text-gray-500">Brak aktywnych nawyków.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-white rounded-2xl shadow p-5 border border-purple-50">
        <p class="text-gray-500 text-sm">📋 Wszystkie</p>
        <p class="text-3xl font-bold text-gray-900">{{ habits.length }}</p>
      </div>

      <div class="bg-white rounded-2xl shadow p-5 border border-purple-50">
        <p class="text-gray-500 text-sm">🔥 Aktywne</p>
        <p class="text-3xl font-bold text-green-600">{{ activeCount }}</p>
      </div>

      <div class="bg-white rounded-2xl shadow p-5 border border-purple-50">
        <p class="text-gray-500 text-sm">✅ Dzisiaj</p>
        <p class="text-3xl font-bold text-purple-600">{{ completedTodayCount }}</p>
      </div>

      <div class="bg-white rounded-2xl shadow p-5 border border-purple-50">
        <p class="text-gray-500 text-sm">📈 Postęp dnia</p>
        <p class="text-3xl font-bold text-purple-600">{{ todayProgress }}%</p>
      </div>
    </div>

    <div v-if="showAddForm" class="bg-white p-6 rounded-2xl shadow-md mb-8 border border-purple-100">
      <h2 class="text-2xl font-semibold mb-4">Utwórz nowy nawyk</h2>

      <form @submit.prevent="addHabit" class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-gray-700 font-medium mb-2">Nazwa nawyku</label>
          <input
            v-model="newHabit.name"
            type="text"
            placeholder="np. Wypić wodę"
            class="w-full px-4 py-3 border rounded-xl focus:outline-none focus:border-purple-600"
            required
          />
        </div>

        <div>
          <label class="block text-gray-700 font-medium mb-2">Opis</label>
          <input
            v-model="newHabit.description"
            type="text"
            placeholder="Opcjonalny opis"
            class="w-full px-4 py-3 border rounded-xl focus:outline-none focus:border-purple-600"
          />
        </div>

        <div class="flex items-end gap-3">
          <button type="submit" class="flex-1 bg-purple-600 text-white py-3 rounded-xl hover:bg-purple-700">
            Zapisz
          </button>

          <button type="button" @click="showAddForm = false" class="flex-1 bg-gray-200 text-gray-800 py-3 rounded-xl hover:bg-gray-300">
            Anuluj
          </button>
        </div>
      </form>
    </div>

    <div class="bg-white p-5 rounded-2xl shadow-md mb-8 border border-purple-100">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <input
          v-model="searchQuery"
          @input="performSearch"
          type="text"
          placeholder="Szukaj po nazwie..."
          class="px-4 py-3 border rounded-xl focus:outline-none focus:border-purple-600"
        />

        <select
          v-model="filterStatus"
          @change="applyFilter"
          class="px-4 py-3 border rounded-xl focus:outline-none focus:border-purple-600"
        >
          <option value="">Wszystkie nawyki</option>
          <option value="active">Tylko aktywne</option>
          <option value="inactive">Tylko nieaktywne</option>
        </select>

        <button @click="loadAll" class="bg-purple-50 text-purple-700 px-4 py-3 rounded-xl hover:bg-purple-100">
          Odśwież
        </button>
      </div>
    </div>

    <div v-if="message" class="bg-green-100 text-green-800 p-4 rounded-xl mb-6">
      {{ message }}
    </div>

    <div v-if="error" class="bg-red-100 text-red-800 p-4 rounded-xl mb-6">
      {{ error }}
    </div>

    <div v-if="loading" class="text-center py-10 text-gray-600">
      Ładowanie nawyków...
    </div>

    <div v-else-if="habits.length > 0" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      <div
        v-for="habit in habits"
        :key="habit.id"
        class="bg-white rounded-3xl shadow-md p-6 border border-purple-100 hover:shadow-lg transition"
      >
        <div class="flex items-start justify-between gap-4 mb-4">
          <div>
            <h3 class="text-2xl font-bold text-gray-900">{{ habit.name }}</h3>
            <p v-if="habit.description" class="text-gray-600 mt-1">
              {{ habit.description }}
            </p>
          </div>

          <span
            :class="habit.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-700'"
            class="text-xs px-3 py-1 rounded-full font-semibold"
          >
            {{ habit.is_active ? "Aktywny" : "Nieaktywny" }}
          </span>
        </div>

        <div class="mb-4">
          <div class="flex justify-between text-sm text-gray-600 mb-2">
            <span>Postęp ostatnich 7 dni</span>
            <span>{{ habitProgress(habit.id).done }} / 7 dni</span>
          </div>

          <div class="w-full bg-purple-100 rounded-full h-3 overflow-hidden mb-3">
            <div
              class="bg-purple-600 h-3 rounded-full"
              :style="{ width: habitProgress(habit.id).percent + '%' }"
            ></div>
          </div>

          <div class="flex justify-between gap-1">
            <div
              v-for="day in lastSevenDays"
              :key="`${habit.id}-${day.date}`"
              class="flex flex-col items-center gap-1"
            >
              <div
                :class="isCompletedOnDate(habit.id, day.date) ? 'bg-purple-600 text-white' : 'bg-purple-100 text-purple-700'"
                class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold"
              >
                {{ isCompletedOnDate(habit.id, day.date) ? "✓" : "○" }}
              </div>
              <span class="text-[10px] text-gray-500">{{ day.label }}</span>
            </div>
          </div>

          <p class="text-sm text-gray-600 mt-3">
            🔥 Seria: <span class="font-semibold">{{ streak(habit.id) }}</span> dni
          </p>
        </div>

        <div class="bg-purple-50 rounded-2xl p-4 mb-4">
          <label class="block text-sm font-semibold text-gray-700 mb-2">
            Data wykonania
          </label>

          <input
            v-model="selectedDates[habit.id]"
            type="date"
            :max="today"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-purple-600"
          />

          <label class="block text-sm font-semibold text-gray-700 mt-3 mb-2">
            Notatka
          </label>

          <input
            v-model="notes[habit.id]"
            type="text"
            placeholder="Opcjonalna notatka"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-purple-600"
          />

          <button
            @click="markComplete(habit.id)"
            class="w-full mt-4 bg-green-600 text-white px-4 py-3 rounded-xl hover:bg-green-700"
          >
            Oznacz jako wykonany
          </button>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <button @click="toggleActive(habit)" class="bg-yellow-500 text-white px-4 py-2 rounded-xl hover:bg-yellow-600">
            {{ habit.is_active ? "Dezaktywuj" : "Aktywuj" }}
          </button>

          <button @click="viewHistory(habit)" class="bg-blue-600 text-white px-4 py-2 rounded-xl hover:bg-blue-700">
            Historia
          </button>

          <button @click="startEdit(habit)" class="bg-purple-600 text-white px-4 py-2 rounded-xl hover:bg-purple-700">
            Edytuj
          </button>

          <button @click="deleteHabit(habit.id)" class="bg-red-600 text-white px-4 py-2 rounded-xl hover:bg-red-700">
            Usuń
          </button>
        </div>
      </div>
    </div>

    <div v-else class="bg-white rounded-3xl shadow p-12 text-center">
      <p class="text-gray-600 text-lg mb-4">Nie znaleziono nawyków.</p>
      <button @click="showAddForm = true" class="bg-purple-600 text-white px-6 py-3 rounded-xl hover:bg-purple-700">
        Utwórz pierwszy nawyk
      </button>
    </div>

    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white p-8 rounded-3xl max-w-md w-full">
        <h2 class="text-2xl font-bold mb-4">Edytuj nawyk</h2>

        <label class="block text-gray-700 font-medium mb-2">Nazwa</label>
        <input v-model="editingHabit.name" type="text" class="w-full px-4 py-3 border rounded-xl mb-4" />

        <label class="block text-gray-700 font-medium mb-2">Opis</label>
        <textarea v-model="editingHabit.description" class="w-full px-4 py-3 border rounded-xl mb-4" rows="3"></textarea>

        <div class="flex gap-3">
          <button @click="saveEdit" class="flex-1 bg-purple-600 text-white py-3 rounded-xl hover:bg-purple-700">
            Zapisz
          </button>

          <button @click="showEditModal = false" class="flex-1 bg-gray-300 text-gray-800 py-3 rounded-xl hover:bg-gray-400">
            Anuluj
          </button>
        </div>
      </div>
    </div>

    <div v-if="showHistoryModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white p-8 rounded-3xl max-w-lg w-full">
        <h2 class="text-2xl font-bold mb-2">
          Historia: {{ selectedHabit?.name }}
        </h2>

        <p class="text-gray-600 mb-4">
          Filtruj historię wykonania według zakresu dat.
        </p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
          <input v-model="historyStartDate" type="date" :max="today" class="w-full px-4 py-2 border rounded-lg" />
          <input v-model="historyEndDate" type="date" :max="today" class="w-full px-4 py-2 border rounded-lg" />
        </div>

        <button @click="loadHistory" class="w-full bg-purple-600 text-white py-3 rounded-xl hover:bg-purple-700 mb-5">
          Zastosuj filtr
        </button>

        <div v-if="completions.length > 0" class="space-y-3 max-h-96 overflow-y-auto">
          <div
            v-for="completion in completions"
            :key="completion.id"
            class="border border-green-100 bg-green-50 rounded-xl p-4"
          >
            <p class="font-bold text-green-800">
              {{ completion.completion_date }}
            </p>

            <p v-if="completion.notes" class="text-gray-700 mt-1">
              Notatka: {{ completion.notes }}
            </p>
          </div>
        </div>

        <div v-else class="text-gray-600 text-center py-6">
          📅 Brak wykonanych dni dla tego nawyku.
        </div>

        <button @click="showHistoryModal = false" class="w-full mt-5 bg-gray-300 text-gray-800 py-3 rounded-xl hover:bg-gray-400">
          Zamknij
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import { storeToRefs } from "pinia";
import { useHabitStore } from "@/stores/habit";

const habitStore = useHabitStore();
const { habits, completions, loading, error } = storeToRefs(habitStore);

const showAddForm = ref(false);
const showHistoryModal = ref(false);
const showEditModal = ref(false);

const selectedHabit = ref<any>(null);
const selectedDates = ref<Record<string, string>>({});
const notes = ref<Record<string, string>>({});
const completionMap = ref<Record<string, any[]>>({});

const searchQuery = ref("");
const filterStatus = ref("");
const historyStartDate = ref("");
const historyEndDate = ref("");
const message = ref("");

const today = new Date().toISOString().split("T")[0];

const newHabit = ref({
  name: "",
  description: "",
});

const editingHabit = ref({
  id: "",
  name: "",
  description: "",
});

const activeHabits = computed(() => habits.value.filter((h) => h.is_active));
const activeCount = computed(() => activeHabits.value.length);

const completedTodayCount = computed(() =>
  activeHabits.value.filter((h) => isCompletedToday(h.id)).length
);

const todayProgress = computed(() => {
  if (activeCount.value === 0) return 0;
  return Math.round((completedTodayCount.value / activeCount.value) * 100);
});

const lastSevenDays = computed(() => {
  const days = [];

  for (let i = 6; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);

    const value = date.toISOString().split("T")[0];
    const label = date.toLocaleDateString("pl-PL", { weekday: "short" });

    days.push({ date: value, label });
  }

  return days;
});

const showMessage = (text: string) => {
  message.value = text;
  setTimeout(() => {
    message.value = "";
  }, 2500);
};

const ensureHabitDefaults = () => {
  habits.value.forEach((habit) => {
    if (!selectedDates.value[habit.id]) selectedDates.value[habit.id] = today;
    if (!notes.value[habit.id]) notes.value[habit.id] = "";
  });
};

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

const loadAll = async () => {
  await habitStore.loadHabits();
  ensureHabitDefaults();
  await loadCompletionMap();
};

const isCompletedOnDate = (habitId: string, date: string) => {
  return (completionMap.value[habitId] || []).some(
    (completion) => completion.completion_date === date
  );
};

const isCompletedToday = (habitId: string) => isCompletedOnDate(habitId, today);

const habitProgress = (habitId: string) => {
  const done = lastSevenDays.value.filter((day) =>
    isCompletedOnDate(habitId, day.date)
  ).length;

  return {
    done,
    percent: Math.round((done / 7) * 100),
  };
};

const streak = (habitId: string) => {
  let result = 0;
  const completionsForHabit = completionMap.value[habitId] || [];

  for (let i = 0; i < 30; i++) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    const value = date.toISOString().split("T")[0];

    const completed = completionsForHabit.some(
      (completion) => completion.completion_date === value
    );

    if (completed) result++;
    else break;
  }

  return result;
};

const addHabit = async () => {
  await habitStore.createHabit(newHabit.value);
  newHabit.value = { name: "", description: "" };
  showAddForm.value = false;
  await loadAll();
  showMessage("Nawyk został dodany.");
};

const markComplete = async (habitId: string) => {
  const selectedDate = selectedDates.value[habitId] || today;

  if (selectedDate > today) {
    alert("Nie można oznaczać nawyków dla przyszłych dni.");
    return;
  }

  try {
    await habitStore.markComplete(habitId, selectedDate, notes.value[habitId] || "");
    notes.value[habitId] = "";
    await loadAll();
    showMessage("Nawyk oznaczony jako wykonany.");
  } catch (error: any) {
    alert(error.response?.data?.detail || "Nie udało się oznaczyć nawyku.");
  }
};

const quickCompleteToday = async (habitId: string) => {
  selectedDates.value[habitId] = today;
  await markComplete(habitId);
};

const toggleActive = async (habit: any) => {
  await habitStore.updateHabit(habit.id, { is_active: !habit.is_active });
  await loadAll();
  showMessage("Status nawyku został zmieniony.");
};

const startEdit = (habit: any) => {
  editingHabit.value = {
    id: habit.id,
    name: habit.name,
    description: habit.description || "",
  };

  showEditModal.value = true;
};

const saveEdit = async () => {
  await habitStore.updateHabit(editingHabit.value.id, {
    name: editingHabit.value.name,
    description: editingHabit.value.description,
  });

  showEditModal.value = false;
  await loadAll();
  showMessage("Nawyk został zaktualizowany.");
};

const deleteHabit = async (habitId: string) => {
  if (confirm("Usunąć ten nawyk?")) {
    await habitStore.deleteHabit(habitId);
    await loadAll();
    showMessage("Nawyk został usunięty.");
  }
};

const performSearch = async () => {
  if (searchQuery.value.trim()) {
    await habitStore.searchHabits(searchQuery.value);
    ensureHabitDefaults();
    await loadCompletionMap();
  } else {
    await loadAll();
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

  ensureHabitDefaults();
  await loadCompletionMap();
};

const viewHistory = async (habit: any) => {
  selectedHabit.value = habit;
  showHistoryModal.value = true;
  historyStartDate.value = "";
  historyEndDate.value = "";
  await habitStore.loadCompletions(habit.id);
};

const loadHistory = async () => {
  if (!selectedHabit.value) return;

  await habitStore.loadCompletions(
    selectedHabit.value.id,
    historyStartDate.value || undefined,
    historyEndDate.value || undefined
  );
};

onMounted(async () => {
  await loadAll();
});
</script>