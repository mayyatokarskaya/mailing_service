# Dockerfile
FROM python:3.12-slim

# Устанавливаем netcat для проверки БД (используется в entrypoint.sh)
RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем только необходимые файлы для установки зависимостей
COPY pyproject.toml poetry.lock* /app/

# Настраиваем Poetry: устанавливаем зависимости без создания виртуального окружения (чтобы использовать системный Python)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# Копируем весь код
COPY . /app

# Делаем entrypoint.sh исполняемым (если в образе)
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
