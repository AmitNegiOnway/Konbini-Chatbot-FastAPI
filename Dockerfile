# =========================
# Builder Stage
# =========================

FROM python:3.10-slim AS builder

WORKDIR /build

# Build-time system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements first for better Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install \
    --prefix=/install \
    --no-cache-dir \
    -r requirements.txt


# =========================
# Final Stage
# =========================

FROM python:3.10-slim

WORKDIR /konbini

# Runtime dependency required by LightGBM
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# Prevent Python cache files
ENV PYTHONDONTWRITEBYTECODE=1

# Faster Python logs
ENV PYTHONUNBUFFERED=1

# Copy Python packages from builder
COPY --from=builder /install /usr/local

# Copy application files
COPY data ./data
COPY training ./training
COPY app ./app

# Render provides PORT
EXPOSE 5000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-5000}"]