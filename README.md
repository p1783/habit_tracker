# 📅 Habit Tracker

> Projekt wykonany w ramach przedmiotu **Architektura i komunikacja między systemami i bazami danych**

---

# Opis projektu

Habit Tracker jest aplikacją webową umożliwiającą tworzenie, zarządzanie oraz monitorowanie codziennych nawyków.

Projekt został zrealizowany w architekturze klient–serwer z wykorzystaniem technologii REST API. Dane przechowywane są w relacyjnej bazie PostgreSQL, natomiast aplikacja kliencka komunikuje się z serwerem za pomocą protokołu HTTP.

Aplikacja umożliwia pracę zarówno w trybie online, jak i offline. W przypadku utraty połączenia z Internetem dane są przechowywane lokalnie i synchronizowane automatycznie po odzyskaniu połączenia.

---

# Najważniejsze funkcjonalności

### System użytkowników

- rejestracja użytkownika,
- logowanie,
- uwierzytelnianie JWT,
- zarządzanie sesją.

### Zarządzanie nawykami

- dodawanie nowych nawyków,
- edycja nawyków,
- usuwanie nawyków,
- aktywowanie i dezaktywowanie nawyków,
- wyszukiwanie po nazwie,
- filtrowanie aktywnych i nieaktywnych nawyków.

### Monitorowanie realizacji

- oznaczanie wykonania nawyku,
- możliwość oznaczania wcześniejszych dni,
- dodawanie notatek,
- historia wykonania,
- statystyki realizacji,
- aktualna seria,
- najlepsza seria,
- procent wykonania,
- postęp z ostatnich siedmiu dni.

### Tryb offline

- lokalna baza IndexedDB,
- kolejka synchronizacji,
- automatyczna synchronizacja po ponownym połączeniu z Internetem.

---

# Architektura systemu

```
                Vue.js Frontend
                       │
                 Axios REST API
                       │
                 FastAPI Backend
                       │
                 SQLAlchemy ORM
                       │
                  PostgreSQL
```

---

# Zastosowane technologie

## Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT Authentication
- Passlib
- Docker

## Frontend

- Vue 3
- TypeScript
- Vite
- Pinia
- Axios
- Tailwind CSS
- IndexedDB

---

# Struktura projektu

```
habit_tracker
│
├── backend
│   ├── app
│   │   ├── auth
│   │   ├── models
│   │   ├── routes
│   │   ├── schemas
│   │   ├── services
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend
│   ├── src
│   │   ├── router
│   │   ├── services
│   │   ├── stores
│   │   ├── views
│   │   └── App.vue
│   │
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
│
└── README.md
```

---

# Uruchomienie projektu

## Wymagania

- Docker Desktop

lub

- Python 3.11+
- Node.js 18+
- PostgreSQL

---

## Uruchomienie za pomocą Docker

```bash
docker compose up --build
```

Frontend:

```
http://localhost:5173
```

Backend:

```
http://localhost:8000
```

Swagger:

```
http://localhost:8000/docs
```

---

# Dokumentacja API

Backend udostępnia REST API zgodne z dobrymi praktykami projektowania usług sieciowych.

Najważniejsze endpointy obejmują:

### Użytkownicy

- POST /api/auth/register
- POST /api/auth/login

### Habity

- GET /api/habits
- POST /api/habits
- PUT /api/habits/{id}
- DELETE /api/habits/{id}

### Historia

- GET /api/habits/{id}/completions
- POST /api/habits/{id}/completions
- DELETE /api/habits/{id}/completions/{completionId}

Szczegółowa dokumentacja endpointów dostępna jest w Swagger UI:

```
http://localhost:8000/docs
```

---

# Bezpieczeństwo

Aplikacja wykorzystuje uwierzytelnianie oparte o tokeny JWT.

Po poprawnym zalogowaniu użytkownik otrzymuje token dostępu, który jest automatycznie dołączany do kolejnych zapytań HTTP.

---

# Tryb offline

Aplikacja wspiera pracę bez dostępu do Internetu.

W trybie offline:

- dane zapisywane są lokalnie w IndexedDB,
- operacje trafiają do kolejki synchronizacji,
- po odzyskaniu połączenia dane są automatycznie przesyłane do serwera.

---

# Interfejs użytkownika

Aplikacja została zaprojektowana jako prosty, przejrzysty i responsywny interfejs umożliwiający wygodne zarządzanie codziennymi nawykami.

Najważniejsze elementy interfejsu:

- dashboard z podstawowymi statystykami,
- lista nawyków,
- historia wykonania,
- oznaczanie wykonania dla wybranego dnia,
- wyszukiwanie,
- filtrowanie,
- edycja i usuwanie nawyków,
- responsywny układ dostosowany do różnych rozdzielczości.

---

# Przykładowe ekrany aplikacji

> *(w tym miejscu można umieścić zrzuty ekranu aplikacji)*

- ekran logowania,
- rejestracja,
- dashboard,
- lista nawyków,
- historia realizacji,
- Swagger UI.

---

# Repozytorium

Projekt rozwijany był z wykorzystaniem systemu kontroli wersji **Git** oraz repozytorium **GitHub**.

---

# Dokumentacja

Szczegółowa dokumentacja techniczna projektu znajduje się w osobnym pliku PDF dołączonym do projektu.

Dokumentacja zawiera między innymi:

- opis architektury systemu,
- schemat bazy danych,
- dokumentację REST API,
- przykładowe zapytania i odpowiedzi,
- opis synchronizacji,
- opis zastosowanych technologii,
- opis implementacji poszczególnych modułów.

---

# Licencja

Projekt został przygotowany wyłącznie w celach edukacyjnych jako projekt zaliczeniowy na potrzeby przedmiotu:

**Architektura i komunikacja między systemami i bazami danych**