# Builder Stage

FROM python:3.10-slim AS builder

WORKDIR /build

# Install system dependencies only in builder
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy only requirements first (better caching)
COPY requirements.txt .

# Install dependencies into custom folder
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install \
    --prefix=/install \
    --no-cache-dir \
    -r requirements.txt


# Final Stage

FROM python:3.10-slim

WORKDIR /konbini

# Prevent Python cache files
ENV PYTHONDONTWRITEBYTECODE=1

# Faster Python logs
ENV PYTHONUNBUFFERED=1

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy stable folders first
COPY data ./data
COPY training ./training

# Copy frequently changing app last
COPY app ./app

# App port
ENV PORT=5000

EXPOSE 5000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]

