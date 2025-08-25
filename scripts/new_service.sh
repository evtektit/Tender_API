#!/bin/bash
# Скрипт для создания нового сервиса в проекте Docker Compose
# Использование: ./new_service.sh my_service 8010

SERVICE_NAME=$1
PORT=${2:-8000}   # если порт не указан, по умолчанию 8000

if [ -z "$SERVICE_NAME" ]; then
  echo "❌ Укажи имя сервиса!"
  echo "Пример: ./new_service.sh parsers 8010"
  exit 1
fi

# 1. Создаём папку
mkdir -p $SERVICE_NAME
cd $SERVICE_NAME

# 2. Dockerfile
cat > Dockerfile <<EOF
FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD ["python", "main.py"]
EOF

# 3. requirements.txt
echo "fastapi==0.111.0
uvicorn[standard]==0.30.0" > requirements.txt

# 4. main.py
cat > main.py <<EOF
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True, "service": "$SERVICE_NAME"}
EOF

cd ..

# 5. Вставка блока в docker-compose.yml
cat <<EOF

⚡ Добавь в docker-compose.yml блок:

  $SERVICE_NAME:
    build:
      context: ./$SERVICE_NAME
      dockerfile: Dockerfile
    container_name: $SERVICE_NAME
    restart: always
    ports:
      - "$PORT:$PORT"
    networks:
      - tender-net

EOF

echo "✅ Сервис $SERVICE_NAME создан!"
