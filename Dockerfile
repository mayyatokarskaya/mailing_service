FROM python:3.12

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./

COPY . .

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    locales && \
    rm -rf /var/lib/apt/lists/* && \
    locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN pip install --no-cache-dir poetry


RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi


RUN rm -rf /app/media


RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["sh", "/app/entrypoint.sh"]