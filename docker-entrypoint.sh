#!/bin/sh
set -e

echo "Waiting for SQL Server..."
python - <<'PY'
import os
import time

import pyodbc

host = os.environ.get("DB_HOST", "db")
port = os.environ.get("DB_PORT", "1433")
user = os.environ.get("DB_USER", "sa")
password = os.environ.get("DB_PASSWORD", "YourStrong!Passw0rd")
database = os.environ.get("DB_NAME", "hangman_db")
driver = os.environ.get("DB_DRIVER", "ODBC Driver 18 for SQL Server")

master_conn_str = (
    f"DRIVER={{{driver}}};"
    f"SERVER={host},{port};"
    "DATABASE=master;"
    f"UID={user};PWD={password};"
    "Encrypt=no;TrustServerCertificate=yes;"
)

for attempt in range(30):
    try:
        connection = pyodbc.connect(master_conn_str, timeout=3, autocommit=True)
        cursor = connection.cursor()
        cursor.execute(
            f"IF DB_ID(N'{database}') IS NULL CREATE DATABASE [{database}]"
        )
        connection.close()
        print("SQL Server is ready and database exists.")
        break
    except Exception as exc:
        print(f"Attempt {attempt + 1}/30: waiting for SQL Server ({exc})")
        time.sleep(2)
else:
    raise SystemExit("SQL Server is not reachable.")
PY

python manage.py migrate
python manage.py seed_players

exec python manage.py runserver 0.0.0.0:8000
