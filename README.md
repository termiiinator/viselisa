<div align="center">

# ⚽ Hangman — Italian Footballers

**Guess the names of legendary Italian football players, letter by letter.**

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16-red?style=flat-square)](https://www.django-rest-framework.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

</div>

---

## Overview

A full-stack Hangman game built as a Django course project. Each round, a random Italian football legend is chosen as the hidden word. Wrong guesses draw the gallows — and unlock progressive hints about the player (age, position, shirt number, clubs). The game runs entirely in a Django session — no JavaScript framework, no database per request, just clean REST calls from a vanilla frontend.

---

## Features

- **Session-based game engine** — state lives server-side, no local storage needed
- **Progressive hint system** — each mistake reveals one more clue in a fixed order: age → position → shirt number → first club → current club
- **6-mistake limit** with SVG gallows animation
- **Dual-database support** — SQLite out of the box, Microsoft SQL Server for production
- **Static files via WhiteNoise** — single-process deployment, no Nginx required
- **Management command** to seed / reset players table

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12+ |
| Web framework | Django 6.0.1 |
| REST API | Django REST Framework 3.16 |
| Database | SQLite (dev) · Microsoft SQL Server (prod) |
| Static files | WhiteNoise 6.11 |
| Frontend | Vanilla HTML · CSS · JavaScript |
| WSGI server | Gunicorn |
| Config | python-dotenv |

---

## Project Structure

```
viselisa/
├── backend_project/          # Django project package
│   ├── settings.py           # All config via environment variables
│   ├── urls.py
│   └── wsgi.py
├── game/                     # Core application
│   ├── models.py             # Player model (name, age, position, number, clubs)
│   ├── views.py              # NewGameView · GuessLetterView · home_view
│   ├── serializers.py
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── seed_players.py   # Populates 10 Italian legends
├── frontend/                 # Static UI (served by WhiteNoise)
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── .env.example              # Copy to .env and fill in your values
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── manage.py
```

---

## API

All game logic goes through three endpoints. Game state is persisted in the Django session.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/game/new/` | Start a new game — picks a random player, resets session state |
| `POST` | `/api/game/guess/` | Submit a letter — body: `{"letter": "a"}` |
| `GET` | `/api/players/random/` | Fetch a random player record (utility) |

**Guess response shape:**

```json
{
  "masked_word":       "_ u _ _ o n",
  "mistakes":          2,
  "max_mistakes":      6,
  "guessed_letters":   ["u", "n"],
  "wrong_letters":     ["x", "z"],
  "hints":             [{"label": "Age", "value": "47"}],
  "status":            "ongoing",
  "repeated":          false,
  "word":              null
}
```

`status` is one of `ongoing` · `won` · `lost`. `word` is revealed only when the game ends.

---

## Getting Started

### Prerequisites

- Python 3.12+
- pip

### 1 — Clone

```bash
git clone https://github.com/Rinat5x30/viselisa.git
cd viselisa
```

### 2 — Virtual environment & dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3 — Environment variables

```bash
cp .env.example .env
```

Open `.env` and set at least `SECRET_KEY`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
USE_SQLITE_FALLBACK=1
```

Need a fresh secret key?

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4 — Database & seed

```bash
python manage.py migrate
python manage.py seed_players
```

### 5 — Run

```bash
python manage.py runserver
```

Visit **http://localhost:8000**

---

## Docker

```bash
docker compose up --build
```

The container automatically runs `migrate`, `seed_players`, then starts Gunicorn on port **8000**. No extra configuration needed — SQLite is used by default.

---

## SQL Server (Production)

Set `USE_SQLITE_FALLBACK=0` and provide credentials in `.env`:

```env
USE_SQLITE_FALLBACK=0
DB_NAME=hangman_db
DB_USER=sa
DB_PASSWORD=YourStrong!Passw0rd
DB_HOST=localhost
DB_PORT=1433
DB_DRIVER=ODBC Driver 18 for SQL Server
```

Also install `mssql-django` and the [ODBC Driver 18](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server) for your OS.

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | ✅ | — | Django cryptographic secret |
| `DEBUG` | | `False` | Enable debug mode |
| `ALLOWED_HOSTS` | | `localhost,127.0.0.1` | Comma-separated allowed hosts |
| `USE_SQLITE_FALLBACK` | | `1` | `1` = SQLite · `0` = SQL Server |
| `DB_NAME` | | `hangman_db` | SQL Server database |
| `DB_USER` | | `sa` | SQL Server user |
| `DB_PASSWORD` | if MSSQL | — | SQL Server password |
| `DB_HOST` | | `localhost` | SQL Server host |
| `DB_PORT` | | `1433` | SQL Server port |
| `DB_DRIVER` | | `ODBC Driver 18 for SQL Server` | ODBC driver string |

---

## Seeded Players

Ten Italian legends loaded by `seed_players`:

| Player | Position | Club |
|---|---|---|
| Buffon | Goalkeeper | Retired |
| Maldini | Defender | Retired |
| Totti | Forward | Retired |
| Del Piero | Forward | Retired |
| Pirlo | Midfielder | Retired |
| Chiellini | Defender | Los Angeles FC |
| Bonucci | Defender | Fenerbahçe |
| Verratti | Midfielder | Al Arabi |
| Barella | Midfielder | Inter |
| Donnarumma | Goalkeeper | Paris Saint-Germain |

```bash
python manage.py seed_players          # insert missing only
python manage.py seed_players --reset  # wipe and re-seed
```

---

## License

[MIT](LICENSE)
