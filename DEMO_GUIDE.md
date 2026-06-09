# DEMO & Testing Guide - Habit Tracker

## 🎬 Demo Scenariusz

Kroki do demonstracji pełnej funkcjonalności aplikacji:

### 1. Setup & Uruchomienie

```bash
# Klonuj repozytorium
git clone https://github.com/p1783/habit_tracker.git
cd habit_tracker

# Uruchom z Docker Compose
docker-compose up -d

# Czekaj aż wszystko się uruchomi (~30 sekund)
docker-compose logs -f
```

### 2. Rejestracja

1. Otwórz: http://localhost:5173
2. Kliknij "Register"
3. Wypełnij formularz:
   - Email: `demo@example.com`
   - Username: `demo_user`
   - Password: `DemoPassword123`
4. Kliknij "Register"
5. System automatycznie przekieruje do logowania

### 3. Logowanie

1. Wpisz email: `demo@example.com`
2. Wpisz password: `DemoPassword123`
3. Kliknij "Login"
4. Zostaniesz przekierowany do panelu głównego

### 4. Tworzenie nawyków

#### Nawyk 1: Morning Exercise
1. Kliknij "+ Add Habit"
2. Wypełnij:
   - Habit Name: `Morning Exercise`
   - Description: `30 minutes of jogging or exercise`
   - Frequency: `daily`
3. Kliknij "Create"

#### Nawyk 2: Reading
1. Kliknij "+ Add Habit"
2. Wypełnij:
   - Habit Name: `Read Book`
   - Description: `Read at least 30 pages`
   - Frequency: `daily`
3. Kliknij "Create"

#### Nawyk 3: Meditation
1. Kliknij "+ Add Habit"
2. Wypełnij:
   - Habit Name: `Meditation`
   - Description: `10 minutes of meditation`
   - Frequency: `daily`
3. Kliknij "Create"

### 5. Oznaczanie wykonań

1. Dla "Morning Exercise" kliknij "✓ Complete Today"
2. Wpisz notatki: `Ran for 35 minutes at the park`
3. Kliknij "OK"
4. Dla "Read Book" kliknij "✓ Complete Today"
5. Wpisz notatki: `Finished chapter 5`
6. Kliknij "OK"

**Rezultat:** Dwa nawyki będą oznaczone jako wykonane

### 6. Filtrowanie nawyków

1. Zmień filter na "Active" - powinny być widoczne wszystkie 3 nawyki
2. Zmień filter na "Inactive" - powinien być pusty
3. Zmień z powrotem na "All Habits"

### 7. Wyszukiwanie

1. Wpisz w pole wyszukiwania: `Read`
2. System pokaże tylko nawyk "Read Book"
3. Wyczyść pole wyszukiwania

### 8. Historia wykonań

1. Dla nawyku "Morning Exercise" kliknij "📊 History"
2. Okno modalne pokaże:
   - Data wykonania: dzisiejsza data
   - Notatka: "Ran for 35 minutes at the park"
3. Kliknij "Close"

### 9. Edycja nawyku

1. Dla nawyku "Meditation" kliknij "✏️" (edycja)
2. Zmień nazwę na: `Morning Meditation`
3. Zmień opis na: `15 minutes of meditation`
4. Kliknij "Save"
5. Nawyk będzie zaktualizowany

### 10. Dezaktywacja nawyku

1. Dla nawyku "Meditation" kliknij "⊘ Deactivate"
2. Nawyk zmieni status na nieaktywny
3. Kliknij "✓ Activate" aby go ponownie aktywować

### 11. Filtrowanie po dacie

1. Dla nawyku "Morning Exercise" kliknij "📊 History"
2. Ustaw:
   - Start Date: dzisiejsza data
   - End Date: dzisiejsza data
3. Kliknij "Apply Filter"
4. Historia powinna pokazać tylko wykonania z dzisiaj

### 12. Usuwanie wykonania

1. W historii nawyku "Morning Exercise" kliknij "Remove"
2. Potwierdź usunięcie
3. Wykonanie zostanie usunięte

### 13. Usuwanie nawyku

1. Dla nawyku "Meditation" kliknij "🗑️" (usuń)
2. Potwierdź usunięcie
3. Nawyk zostanie usunięty ze listy

### 14. Tryb Offline

1. Otwórz DevTools (F12) w przeglądarce
2. Przejdź do Network tab
3. Zmień na "Offline" mode
4. Zauważ wskaźnik "📡 Offline Mode" w górnej części
5. Spróbuj utworzyć nowy nawyk - zostanie zapisany offline
6. Zmień network na "Online"
7. Aplikacja automatycznie zsynchronizuje dane

## 🧪 Testowanie API (Curl)

### 1. Rejestracja
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPassword123"
  }'
```

### 2. Logowanie
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123"
  }' | jq -r '.access_token')

echo "Token: $TOKEN"
```

### 3. Tworzenie nawyku
```bash
curl -X POST http://localhost:8000/api/habits \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Exercise",
    "description": "Daily exercise",
    "frequency": "daily"
  }'
```

### 4. Pobieranie nawyków
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/habits
```

### 5. Wyszukiwanie
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/habits/search?query=Exercise"
```

### 6. Filtrowanie
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/habits?is_active=true"
```

### 7. Oznaczanie jako wykonane
```bash
HABIT_ID="<habit_id_z_poprzedniego_kroku>"

curl -X POST http://localhost:8000/api/habits/$HABIT_ID/completions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "completion_date": "2026-06-09",
    "notes": "Completed successfully"
  }'
```

### 8. Historia wykonań
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/habits/$HABIT_ID/completions"
```

### 9. Historia z filtrem po dacie
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/habits/$HABIT_ID/completions?start_date=2026-06-01&end_date=2026-06-30"
```

## 📊 Swagger UI Demo

1. Otwórz: http://localhost:8000/docs
2. System pokaże interaktywną dokumentację API
3. Możesz testować każdy endpoint bezpośrednio z interfejsu:
   - Kliknij na endpoint
   - Kliknij "Try it out"
   - Wpisz parametry
   - Kliknij "Execute"

## 📱 Browser DevTools

### Network Tab
1. Otwórz DevTools (F12)
2. Przejdź do Network tab
3. Wykonaj akcje w aplikacji
4. Obserwuj żądania HTTP
5. Sprawdź request/response headers i body

### Application Tab
1. Przejdź do Application tab
2. Sprawdź IndexedDB:
   - HabitTrackerDB
   - Tabele: habits, completions, syncQueue
3. Sprawdź Local Storage:
   - Token JWT
4. Sprawdź Cookies

### Console Tab
1. Sprawdź czy nie ma błędów
2. Sprawdzaj logi aplikacji

## ✅ Checklist Funkcjonalności

- [ ] Rejestracja użytkownika działa
- [ ] Logowanie działa
- [ ] Tworzenie nawyków działa
- [ ] Edycja nawyków działa
- [ ] Usuwanie nawyków działa
- [ ] Oznaczanie wykonań działa
- [ ] Historia wykonań wyświetla się
- [ ] Notatki są dodawane
- [ ] Filtrowanie aktywnych/nieaktywnych
- [ ] Wyszukiwanie po nazwie
- [ ] Filtrowanie po dacie
- [ ] Usuwanie wykonań działa
- [ ] Tryb offline działa
- [ ] Synchronizacja offline→online
- [ ] JWT autentykacja zabezpiecza API
- [ ] Komunikaty błędów wyświetlają się
- [ ] UI jest responsywny
- [ ] Swagger UI dokumentacja dostępna

## 🐛 Troubleshooting

### Problem: Port 5173 jest zajęty
```bash
# Zmień port w frontend/vite.config.ts lub uruchom na innym porcie
npm run dev -- --port 3000
```

### Problem: Port 8000 jest zajęty
```bash
# Zmień port w .env lub uruchom na innym porcie
uvicorn app.main:app --reload --port 8001
```

### Problem: Baza danych nie połączy się
```bash
# Sprawdź czy PostgreSQL kontener jest uruchomiony
docker-compose ps

# Restart kontenerów
docker-compose restart
```

### Problem: Token wygasł
```bash
# Wyloguj się i zaloguj ponownie
# Token jest ważny przez 30 minut
```

### Problem: Offline mode nie działa
```bash
# Sprawdź czy przeglądarka obsługuje IndexedDB
# Sprawdź DevTools → Application → IndexedDB
```

## 📝 Notes

- Demo data są usuwane po czyszczeniu bazy
- Tokeny JWT wygasają po 30 minutach
- Offline queue synchronizuje się automatycznie po powrocie online
- Każdy nawyk może mieć maksymalnie jedno wykonanie dziennie
