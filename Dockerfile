FROM python:3.12

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app


RUN pip install --no-cache-dir poetry


COPY pyproject.toml poetry.lock README.md ./


RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi


COPY . /app

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
