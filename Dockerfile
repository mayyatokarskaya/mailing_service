FROM python:3.12

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app


RUN pip install --no-cache-dir poetry


COPY pyproject.toml poetry.lock* /app/


RUN poetry check && \
    poetry lock --no-update && \
    poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main


COPY . /app

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
