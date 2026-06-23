<template>
  <div class="max-w-5xl mx-auto">
    <div class="bg-white rounded-3xl shadow-lg p-8 mb-8">
      <p class="text-sm font-semibold text-purple-600 mb-2">Panel dzisiejszych nawyków</p>

      <h1 class="text-4xl font-bold text-gray-900 mb-3">
        Witaj w Habit Trackerze
      </h1>

      <p class="text-gray-600 text-lg mb-6">
        Zarządzaj nawykami, oznaczaj wykonanie i analizuj swoją historię.
      </p>

      <router-link
        to="/habits"
        class="inline-block bg-purple-600 text-white px-6 py-3 rounded-xl hover:bg-purple-700 shadow-md"
      >
        Przejdź do nawyków
      </router-link>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
      <div class="bg-purple-50 rounded-2xl p-6">
        <p class="text-purple-700 font-semibold">REST API</p>
        <p class="text-gray-600 mt-2">Aplikacja komunikuje się z backendem FastAPI.</p>
      </div>

      <div class="bg-purple-50 rounded-2xl p-6">
        <p class="text-purple-700 font-semibold">Baza danych</p>
        <p class="text-gray-600 mt-2">Dane użytkowników, nawyków i historii są w PostgreSQL.</p>
      </div>

      <div class="bg-purple-50 rounded-2xl p-6">
        <p class="text-purple-700 font-semibold">Offline MVP</p>
        <p class="text-gray-600 mt-2">Projekt zawiera IndexedDB i kolejkę synchronizacji.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>