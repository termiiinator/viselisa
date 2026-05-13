# Hangman: Italian Footballers

A web-based Hangman game where you guess the names of famous Italian football players. Built with Django and Django REST Framework, featuring a session-based game engine and a clean vanilla-JS frontend.

## Features

- Random player selection from a seeded database of Italian legends
- Progressive hints revealed on each wrong guess (age → position → number → clubs)
- REST API for game logic — new game, guess a letter
- Dual-database support: SQLite for local development, SQL Server (MSSQL) for production
- Static file serving via WhiteNoise — no extra web server needed

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0.1, Django REST Framework 3.16 |
| Database | SQLite (dev) / Microsoft SQL Server (prod) |
| Static files | WhiteNoise 6.11 |
| Frontend | Vanilla HTML / CSS / JavaScript |
| Server | Gunicorn |

## Project Structure

```
backend_project/
├── backend_project/      # Django project config (settings, urls, wsgi)
├── game/                 # Core app
│   ├── models.py         # Player model
│   ├── views.py          # API views + home view
│   ├── serializers.py
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── seed_players.py   # Loads 10 Italian players
├── frontend/             # HTML / CSS / JS served as static files
├── .env.example          # Environment variable template
├── requirements.txt
└── manage.py
```

## API Endpoints

| Method | URL | Description |
|---|---|---|
| `GET` | `/api/players/random/` | Get a random player |
| `POST` | `/api/game/new/` | Start a new game session |
| `POST` | `/api/game/guess/` | Guess a letter `{"letter": "a"}` |

Game state is stored in the Django session (`request.session`).

## Quick Start

### 1. Clone and set up the environment

```bash
git clone https://github.com/Rinat5x30/viselisa.git
cd viselisa
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` — at minimum set a strong `SECRET_KEY`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
USE_SQLITE_FALLBACK=1
```

Generate a secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Run migrations and seed players

```bash
python manage.py migrate
python manage.py seed_players
```

### 4. Start the development server

```bash
python manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

## SQL Server Setup (optional)

Set `USE_SQLITE_FALLBACK=0` in `.env` and fill in the SQL Server credentials:

```env
USE_SQLITE_FALLBACK=0
DB_NAME=hangman_db
DB_USER=sa
DB_PASSWORD=YourStrong!Passw0rd
DB_HOST=localhost
DB_PORT=1433
DB_DRIVER=ODBC Driver 18 for SQL Server
```

Requires the `mssql-django` package and the appropriate ODBC driver installed on the host.

## Docker Compose

```bash
docker compose up --build
```

The `web` container automatically runs migrations, seeds the players table, and starts Django on port 8000.

## Environment Variables Reference

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | **required** | Django secret key |
| `DEBUG` | `False` | Enable debug mode |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated list of allowed hosts |
| `USE_SQLITE_FALLBACK` | `1` | `1` = SQLite, `0` = SQL Server |
| `DB_NAME` | `hangman_db` | SQL Server database name |
| `DB_USER` | `sa` | SQL Server user |
| `DB_PASSWORD` | **required if MSSQL** | SQL Server password |
| `DB_HOST` | `localhost` | SQL Server host |
| `DB_PORT` | `1433` | SQL Server port |
| `DB_DRIVER` | `ODBC Driver 18 for SQL Server` | ODBC driver name |

## Seeded Players

The `seed_players` command loads 10 iconic Italian players:
Buffon, Maldini, Totti, Del Piero, Pirlo, Chiellini, Bonucci, Verratti, Barella, Donnarumma.

```bash
python manage.py seed_players         # add only missing players
python manage.py seed_players --reset # wipe and re-seed
```

## License

MIT
