FROM node:22-alpine AS web-dependencies
WORKDIR /build/apps/web
COPY apps/web/package.json apps/web/package-lock.json ./
RUN npm ci

FROM web-dependencies AS web-builder
COPY apps/web/ ./
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OMP_THREAD_LIMIT=1 \
    STATIC_DIR=/app/static \
    PORT=8000
WORKDIR /app

RUN apt-get update \
    && apt-get install --yes --no-install-recommends tesseract-ocr tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*
RUN addgroup --system --gid 1001 labelguard \
    && adduser --system --uid 1001 --ingroup labelguard labelguard
COPY apps/api /tmp/api
RUN pip install --no-cache-dir /tmp/api \
    && rm -rf /tmp/api
COPY --from=web-builder /build/apps/web/out ./static

USER labelguard
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=3)"
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
