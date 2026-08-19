FROM python:3.14 AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml
COPY ./uv.lock /code/uv.lock

RUN uv sync

FROM python:3.14-slim AS runner

RUN apt-get update \
    && apt-get install -y --no-install-recommends eject \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY --from=builder /code/.venv /code/.venv

ENV PATH=/code/.venv/bin:$PATH

COPY ./main.py /code/main.py

CMD ["fastapi", "run", "main.py", "--port", "7000"]