# Habit Tracker - Aplikacja do zarządzania nawykami

Kompleksowa aplikacja do tworzenia, zarządzania i monitorowania codziennych nawyków. System wykorzystuje architekturę klient-serwer z REST API.

## 📋 Spis treści

- [Architektura](#architektura)
- [Technologia](#technologia)
- [Instalacja](#instalacja)
- [Uruchamianie](#uruchamianie)
- [Struktura projektu](#struktura-projektu)
- [API Documentation](#api-documentation)

## 🏗️ Architektura

```
┌─────────────────────────────────────────────┐
│         Frontend (Vue.js)                    │
│  - UI dla zarządzania nawykami              │
│  - Tryb offline (IndexedDB)                 │
│  - Synchronizacja danych                    │
└──────────────┬─────────────────��────────────┘
               │ HTTP/REST
┌──────────────▼──────────────────────────────┐
│         Backend (Python/FastAPI)             │
│  - REST API                                 │
│  - JWT Authentication                       │
│  - Zarządzanie habitami                     │
│  - Synchronizacja offline                   │
└──────────────┬──────────────────────────────┘
               │ SQL
┌──────────────▼──────────────────────────────┐
│     Database (PostgreSQL)                    │
│  - Users                                    │
│  - Habits                                   │
│  - Habit Completions                        │
└──────────────────────────────────────────────┘
```

## 💻 Technologia

### Backend
- **Framework**: FastAPI (Python)
- **Baza danych**: PostgreSQL
- **ORM**: SQLAlchemy
- **Autentykacja**: JWT (PyJWT)
- **Walidacja**: Pydantic
- **CORS**: fastapi-cors

### Frontend
- **Framework**: Vue.js 3
- **Build tool**: Vite
- **HTTP Client**: Axios
- **Offline Storage**: IndexedDB
- **Styling**: Tailwind CSS

## 📁 Struktura projektu

```
habit_tracker/
├── backend/                 # Python FastAPI aplikacja
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # Główna aplikacja
│   │   ├── config.py       # Konfiguracja
│   │   ├── models/         # Modele ORM
│   │   ├── schemas/        # Pydantic schemas (DTO)
│   │   ├── routes/         # Endpointy API
│   │   ├── services/       # Logika biznesowa
│   │   ├── database.py     # Konfiguracja bazy
│   │   └── auth/           # Autentykacja JWT
│   ├── tests/              # Testy jednostkowe
│   ├── requirements.txt    # Zależności Python
│   ├── .env.example        # Przykład zmiennych środowiska
│   └── README.md           # Dokumentacja backendu
│
├── frontend/               # Vue.js aplikacja
│   ├── src/
│   │   ├── components/     # Vue komponenty
│   │   ├── views/          # Strony aplikacji
│   │   ├── services/       # API client, offline storage
│   │   ├── stores/         # State management (Pinia)
│   │   ├── App.vue         # Główny komponent
│   │   └── main.js         # Entry point
│   ├── public/             # Zasoby statyczne
│   ├── package.json        # Zależności npm
│   ├── vite.config.js      # Konfiguracja Vite
│   └── README.md           # Dokumentacja frontendu
│
├── docker-compose.yml      # Konfiguracja kontenerów
├── .gitignore              # Git ignore
└── README.md               # Ten plik
```

## 🚀 Instalacja

### Wymagania
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Docker i Docker Compose (opcjonalnie)

### Szybki start z Docker

```bash
# Klonowanie repozytorium
git clone https://github.com/p1783/habit_tracker.git
cd habit_tracker

# Uruchomienie za pomocą Docker Compose
docker-compose up -d

# Backend będzie dostępny na: http://localhost:8000
# Frontend będzie dostępny na: http://localhost:3000
# API Docs (Swagger): http://localhost:8000/docs
```

### Instalacja ręczna

#### Backend

```bash
cd backend

# Tworzenie virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate  # Windows

# Instalacja zależności
pip install -r requirements.txt

# Konfiguracja zmiennych środowiska
cp .env.example .env

# Inicjalizacja bazy danych
python -m alembic upgrade head

# Uruchomienie serwera
uvicorn app.main:app --reload
```

Backend będzie dostępny na `http://localhost:8000`

#### Frontend

```bash
cd frontend

# Instalacja zależności
npm install

# Uruchomienie dev serwera
npm run dev
```

Frontend będzie dostępny na `http://localhost:5173`

## 📚 API Documentation

### Autentykacja

#### Rejestracja
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "username": "username"
}
```

#### Logowanie
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Zarządzanie nawykami

#### Pobieranie listy nawyków
```
GET /api/habits
Authorization: Bearer {token}
```

#### Dodawanie nowego nawyku
```
POST /api/habits
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Czytanie",
  "description": "Codzienne czytanie książki",
  "frequency": "daily"
}
```

#### Oznaczanie wykonania nawyku
```
POST /api/habits/{habit_id}/completions
Authorization: Bearer {token}
Content-Type: application/json

{
  "date": "2026-06-09",
  "notes": "Przeczytałem 30 stron"
}
```

Pełna dokumentacja API dostępna na: `http://localhost:8000/docs` (Swagger UI)

## 🔧 Zmienne środowiska

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/habit_tracker
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["http://localhost:5173"]
```

## 📦 Funkcjonalności

### Zaimplementowane
- [ ] System użytkowników (rejestracja, logowanie, JWT)
- [ ] CRUD operacje na nawykami
- [ ] Monitorowanie realizacji nawyków
- [ ] Wyszukiwanie i filtrowanie nawyków
- [ ] Baza danych PostgreSQL
- [ ] REST API z FastAPI
- [ ] Frontend Vue.js
- [ ] Tryb offline i synchronizacja

## 🧪 Testowanie

```bash
# Backend testy
cd backend
pytest

# Frontend testy
cd frontend
npm run test
```

## 📖 Dokumentacja

- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)
- [API Docs](http://localhost:8000/docs)

## 👨‍💻 Autor

p1783

## 📄 Licencja

MIT
