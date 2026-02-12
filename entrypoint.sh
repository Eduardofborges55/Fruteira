#!/bin/sh

set -e

echo "Aguardando banco de dados..."
python - <<'PY'
import os
import time
import psycopg2

host = os.getenv("POSTGRES_HOST", os.getenv("DB_HOST", "db"))
port = int(os.getenv("POSTGRES_PORT", os.getenv("DB_PORT", "5432")))
name = os.getenv("POSTGRES_DB", os.getenv("DB_NAME", "fruteira"))
user = os.getenv("POSTGRES_USER", os.getenv("DB_USER", "fruteira"))
password = os.getenv("POSTGRES_PASSWORD", os.getenv("DB_PASSWORD", "fruteira"))

for attempt in range(1, 31):
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=name,
            user=user,
            password=password,
        )
        conn.close()
        print("Banco pronto.")
        break
    except Exception as exc:
        print(f"Tentativa {attempt}/30: banco ainda indisponivel ({exc})")
        time.sleep(2)
else:
    raise SystemExit("Nao foi possivel conectar ao banco apos 60s.")
PY

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
