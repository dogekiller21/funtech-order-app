FROM python:3.13-slim
ENV PYTHONPATH="/"
ENV PYTHONUNBUFFERED="1"
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m pip install --no-cache-dir uv
COPY . /app
WORKDIR app/src/

RUN uv sync --dev

CMD ["uv", "run", "--", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
