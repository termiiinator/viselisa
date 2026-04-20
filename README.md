# Hangman: Italian Footballers

Веб-приложение «Виселица» на Django + HTML/CSS/JS.

## Что реализовано

- Загаданное слово — имя/фамилия итальянского футболиста.
- Ввод только одной латинской буквы.
- Повторная буква не штрафуется и игнорируется.
- При ошибке:
  - добавляется элемент виселицы,
  - открывается ровно одна подсказка в порядке:
    1. Возраст
    2. Позиция
    3. Игровой номер
    4. Первый профессиональный клуб
    5. Текущий клуб
- Конец игры:
  - Победа — слово угадано полностью.
  - Поражение — 5 ошибок (виселица завершена).

## Структура

- `backend_project/` — настройки Django проекта.
- `game/` — backend-логика:
  - `models.py` — модель `Player`.
  - `serializers.py` — сериализаторы DRF.
  - `views.py` — API и логика игры через сессию.
  - `urls.py` — маршруты API.
- `frontend/` — клиентская часть:
  - `index.html`
  - `styles.css`
  - `app.js`
- `sql/init_players.sql` — SQL Server скрипт создания и заполнения таблицы `players`.
- `docker-compose.yml` + `Dockerfile` — запуск Django в контейнере с SQLite.

## API

- `POST /api/game/new/` — начать новую игру (выбирается случайный игрок).
- `POST /api/game/guess/` — проверить букву, JSON: `{ "letter": "a" }`.
- `GET /api/players/random/` — получить случайного игрока (служебный API).

Состояние игры хранится в сессии Django (`request.session`).

## Быстрые команды

- Заполнить игроков: `python manage.py seed_players`
- Перезаполнить с очисткой: `python manage.py seed_players --reset`
- Запустить тесты: `python manage.py test`

## Запуск проекта

### 1) Установить зависимости

```bash
pip install -r requirements.txt
```

### 2) Настроить SQLite

SQLite включен по умолчанию через `USE_SQLITE_FALLBACK=1`, дополнительных переменных не нужно.

### 3) Применить миграции Django

```bash
python manage.py migrate
```

### 4) Заполнить таблицу игроков

```bash
python manage.py seed_players
```

### 5) Запустить сервер

```bash
python manage.py runserver
```

Откройте в браузере: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Запуск через Docker Compose

```bash
docker compose up --build
```

Что делает контейнер `web` автоматически:

- выполняет `python manage.py migrate`;
- выполняет `python manage.py seed_players`;
- запускает Django на `0.0.0.0:8000`.
