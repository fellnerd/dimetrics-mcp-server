# Multi-stage build für optimierte Image-Größe
FROM python:3.11-slim as builder

# Build-Dependencies installieren
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis setzen
WORKDIR /app

# Requirements installieren
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

# Runtime-Dependencies installieren
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

# Arbeitsverzeichnis setzen
WORKDIR /app

# Python packages von builder stage kopieren
COPY --from=builder /root/.local /home/mcpuser/.local

# Application code kopieren
COPY dimetrics_mcp_server/ ./dimetrics_mcp_server/
COPY *.py ./
COPY *.md ./
COPY .env.example ./.env.example

# Logs-Verzeichnis erstellen
RUN mkdir -p /app/logs && chown -R mcpuser:mcpuser /app/logs && chown -R mcpuser:mcpuser /home/mcpuser/.local

# Python path erweitern
ENV PATH=/home/mcpuser/.local/bin:$PATH
ENV PYTHONPATH=/app

# Health check script erstellen
RUN echo '#!/bin/bash\ncurl -f http://localhost:${PORT:-8000}/health || exit 1' > /app/healthcheck.sh \
    && chmod +x /app/healthcheck.sh

# Benutzer wechseln
USER mcpuser

# Port exposieren
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD /app/healthcheck.sh

# Default command
CMD ["python3", "-m", "dimetrics_mcp_server"]
