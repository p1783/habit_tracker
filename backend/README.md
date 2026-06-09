# Habit Tracker Backend

REST API backend dla aplikacji Habit Tracker, napisany w FastAPI.

## 🚀 Szybki start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Backend: `http://localhost:8000`

## 📚 Dokumentacja API

Swagger UI: `http://localhost:8000/docs`

## 📁 Struktura projektu

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # Główna aplikacja
│   ├── config.py         # Konfiguracja
│   ├── database.py       # Setup bazy danych
│   ├── models/           # Modele ORM
│   ├── schemas/          # Pydantic schemas
│   ├── routes/           # API endpoints
│   ├── services/         # Logika biznesowa
│   └── auth/             # Autentykacja JWT
├── tests/                # Testy
├── requirements.txt      # Zależności
└── .env.example          # Przykład .env
```

## 📝 API Endpoints

### Auth
- `POST /api/auth/register` - Rejestracja
- `POST /api/auth/login` - Logowanie

### Habits
- `POST /api/habits` - Tworzenie
- `GET /api/habits` - Pobieranie listy
- `GET /api/habits/{id}` - Szczegóły
- `PUT /api/habits/{id}` - Aktualizacja
- `DELETE /api/habits/{id}` - Usuwanie

### Completions
- `POST /api/habits/{id}/completions` - Oznaczenie
- `GET /api/habits/{id}/completions` - Historia
