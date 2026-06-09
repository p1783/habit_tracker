# Habit Tracker - Dokumentacja Projektu

## 📋 Spis treści
1. [Temat](#temat)
2. [Opis projektu](#opis-projektu)
3. [Architektura](#architektura)
4. [Funkcjonalności](#funkcjonalności)
5. [Technologia](#technologia)
6. [Instalacja i uruchomienie](#instalacja-i-uruchomienie)
7. [API Documentation](#api-documentation)

## 🎯 Temat

**Habit Tracker – aplikacja do zarządzania i monitorowania nawyków**

## 📝 Opis projektu

Celem projektu jest stworzenie systemu informatycznego umożliwiającego użytkownikom tworzenie, zarządzanie oraz monitorowanie swoich codziennych nawyków. System będzie składał się z:

- **Serwera** udostępniającego REST API
- **Centralnej bazy danych** (PostgreSQL)
- **Aplikacji klienckiej** (webowej) komunikującej się z serwerem poprzez interfejs API

Aplikacja pozwoli użytkownikom na:
- Dodawanie nowych nawyków
- Oznaczanie ich wykonania w określonych dniach
- Analizowanie historii realizacji nawyków
- Korzystanie z **trybu offline** poprzez lokalną bazę danych (IndexedDB)
- Synchronizację danych z serwerem po odzyskaniu połączenia z internetem

Projekt ma na celu zapoznanie studentów z:
- Architekturą systemów **klient–serwer**
- Komunikacją poprzez **REST API**
- **Zarządzaniem bazą danych**
- **Implementacją uwierzytelniania użytkowników**

## 🏗️ Architektura

```
┌─────────────────────────────────────────────┐
│         Frontend (Vue.js 3)                  │
│  - Interfejs użytkownika                    │
│  - Tryb offline (IndexedDB)                 │
│  - Synchronizacja danych                    │
└──────────────┬──────────────────────────────┘
               │ HTTPS/REST
┌──────────────▼──────────────────────────────┐
│         Backend (Python/FastAPI)             │
│  - REST API z pełną dokumentacją            │
│  - JWT Authentication                       │
│  - Logika biznesowa                         │
│  - Obsługa błędów                           │
└──────────────┬──────────────────────────────┘
               │ SQL
┌──────────────▼──────────────────────────────┐
│     Database (PostgreSQL)                    │
│  - Users (użytkownicy)                      │
│  - Habits (nawyki)                          │
│  - Habit Completions (wykonania nawyków)    │
└──────────────────────────────────────────────┘
```

## ✨ Funkcjonalności

### 1. System użytkowników
- ✅ **Rejestracja nowych użytkowników**
  - Walidacja email i hasła
  - Haszowanie hasła (bcrypt)
  
- ✅ **Logowanie do systemu**
  - Autentykacja emailem i hasłem
  
- ✅ **Uwierzytelnianie przy użyciu tokenów JWT**
  - Bezpieczne tokeny z czasem wygaśnięcia
  - Bearer token w nagłówkach
  
- ✅ **Zarządzanie sesją użytkownika**
  - Automatyczne wylogowanie po wygaśnięciu tokena
  - Obsługa nieautoryzowanych żądań

### 2. Zarządzanie nawykami
- ✅ **Dodawanie nowych nawyków**
  - Nazwa, opis, częstotliwość (daily/weekly)
  - Automatyczne przypisanie do użytkownika
  
- ✅ **Edycja istniejących nawyków**
  - Zmiana nazwy, opisu, częstotliwości
  
- ✅ **Usuwanie nawyków**
  - Kaskadowe usunięcie powiązanych danych
  
- ✅ **Przeglądanie listy wszystkich nawyków użytkownika**
  - Sortowanie i filtrowanie
  
- ✅ **Oznaczanie nawyku jako aktywny lub nieaktywny**
  - Dezaktywacja bez usuwania historii

### 3. Monitorowanie realizacji nawyków
- ✅ **Oznaczanie wykonania nawyku w danym dniu**
  - Zapobieganie duplikatom (jedna ocena na dzień)
  - Walidacja dat
  
- ✅ **Przegląd historii realizacji nawyku**
  - Pełna historia wszystkich wykonań
  
- ✅ **Możliwość dodawania notatek do wykonania nawyku**
  - Opcjonalne notatki dla każdego wykonania
  
- ✅ **Wyświetlanie listy nawyków do wykonania w danym dniu**
  - Filtrowanie wykonań po dacie

### 4. Wyszukiwanie i filtrowanie danych
- ✅ **Wyszukiwanie nawyków po nazwie**
  - Case-insensitive wyszukiwanie
  - Wyszukiwanie w czasie rzeczywistym
  
- ✅ **Filtrowanie nawyków aktywnych i nieaktywnych**
  - Osobne widoki dla aktywnych/nieaktywnych
  - Query parameter filtering
  
- ✅ **Filtrowanie historii wykonania według zakresu dat**
  - Zakresy dat w API
  - Filtrowanie w interfejsie

### 5. Integracja z bazą danych
- ✅ **Przechowywanie danych użytkowników**
  - Tabela `users` z email, username, hashed_password
  - Indeksy na email i username dla szybkości
  
- ✅ **Przechowywanie nawyków użytkowników**
  - Tabela `habits` z relacją do users
  - Pole `is_active` dla dezaktywacji
  
- ✅ **Przechowywanie historii wykonania nawyków**
  - Tabela `habit_completions`
  - Unikalne wykonania na dzień (unique constraint)

### 6. Tryb offline i synchronizacja danych
- ✅ **Przechowywanie danych w lokalnej bazie danych**
  - IndexedDB dla przechowywania offline
  - Automatyczne cachowanie
  
- ✅ **Możliwość korzystania z aplikacji bez dostępu do internetu**
  - Pełna funkcjonalność offline
  - Interfejs pokazujący stan online/offline
  
- ✅ **Synchronizacja danych pomiędzy lokalną bazą danych a serwerem**
  - Automatyczna synchronizacja po powrocie online
  - Queue dla operacji offline
  - Konflikt resolution

### 7. Obsługa błędów
- ✅ **Odpowiednie komunikaty błędów zwracane przez API**
  - Standardowe HTTP status codes (400, 401, 403, 404, 500)
  - Szczegółowe opisy błędów
  - Exception handlers
  - Custom exceptions
  - Frontend error notifications

## 💻 Technologia

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Baza danych**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Autentykacja**: JWT (PyJWT)
- **Haszowanie**: bcrypt
- **Walidacja**: Pydantic
- **CORS**: CORSMiddleware
- **Server**: Uvicorn

### Frontend
- **Framework**: Vue.js 3
- **Build Tool**: Vite
- **State Management**: Pinia
- **Router**: Vue Router 4
- **HTTP Client**: Axios
- **Offline Storage**: IndexedDB
- **Styling**: Tailwind CSS
- **Language**: TypeScript

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Database**: PostgreSQL 15

## 🚀 Instalacja i uruchomienie

### Szybki start z Docker

```bash
# Klonowanie repozytorium
git clone https://github.com/p1783/habit_tracker.git
cd habit_tracker

# Uruchomienie z Docker Compose
docker-compose up -d

# Adresy dostępu:
# - Frontend: http://localhost:5173
# - Backend: http://localhost:8000
# - API Docs (Swagger): http://localhost:8000/docs
# - API Docs (ReDoc): http://localhost:8000/redoc
```

### Instalacja ręczna

#### Backend

```bash
cd backend

# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate      # Windows

# Zainstalowanie zależności
pip install -r requirements.txt

# Konfiguracja
cp .env.example .env
# Edytuj .env z właściwymi wartościami

# Uruchomienie
uvicorn app.main:app --reload
```

Backend będzie dostępny na `http://localhost:8000`

#### Frontend

```bash
cd frontend

# Instalacja zależności
npm install

# Uruchomienie dev server
npm run dev
```

Frontend będzie dostępny na `http://localhost:5173`

## 📚 API Documentation

### Dokumentacja Swagger
Dostępna na: `http://localhost:8000/docs`

### Dokumentacja ReDoc
Dostępna na: `http://localhost:8000/redoc`

### Główne endpointy

#### Authentication
- `POST /api/auth/register` - Rejestracja
- `POST /api/auth/login` - Logowanie

#### Habits
- `POST /api/habits` - Tworzenie nawyku
- `GET /api/habits` - Pobieranie listy nawyków
- `GET /api/habits?is_active=true` - Filtrowanie po statusie
- `GET /api/habits/search?query=...` - Wyszukiwanie
- `GET /api/habits/{id}` - Szczegóły nawyku
- `PUT /api/habits/{id}` - Aktualizacja
- `DELETE /api/habits/{id}` - Usuwanie

#### Completions
- `POST /api/habits/{id}/completions` - Oznaczenie jako wykonane
- `GET /api/habits/{id}/completions` - Historia wykonań
- `GET /api/habits/{id}/completions?start_date=...&end_date=...` - Filtrowanie po dacie
- `DELETE /api/habits/{id}/completions/{completion_id}` - Usuwanie wykonania

## 🧪 Testowanie

```bash
# Backend testy
cd backend
pytest

# Frontend testy
cd frontend
npm run test
```

## 📦 Struktura katalogów

```
habit_tracker/
├── backend/                 # Python FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   ├── handlers.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   ├── services/
│   │   └── auth/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                # Vue.js 3
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── stores/
│   │   ├── services/
│   │   ├── router/
│   │   ├── App.vue
│   │   ├── main.ts
│   │   └── style.css
│   ├── package.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── index.html
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 👨‍💻 Autor

p1783

## 📄 Licencja

MIT
