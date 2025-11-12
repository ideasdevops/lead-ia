# Multi-stage build para Lead-IA
# Stage 1: Build del frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copiar archivos de dependencias
COPY frontend/package*.json ./
RUN npm ci --legacy-peer-deps

# Copiar código fuente y construir
COPY frontend/ ./
RUN npm run build

# Stage 2: Backend con Python
FROM python:3.10-slim

# Instalar dependencias del sistema
# Nota: EasyPanel maneja Nginx automáticamente, no lo instalamos aquí
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorios necesarios
RUN mkdir -p /app/backend \
    /app/frontend/dist \
    /app/logs \
    /app/database

WORKDIR /app

# Copiar requirements del backend
COPY backend/requirements.txt /app/backend/
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Instalar py_lead_generation
# Copiar setup.py, README.md y py_lead_generation al mismo nivel para que find_packages() funcione
COPY setup.py /app/
COPY README.md /app/
COPY py_lead_generation/ /app/py_lead_generation/
WORKDIR /app
RUN pip install --no-cache-dir -e .

# Copiar código del backend
COPY backend/ /app/backend/

# Copiar frontend construido desde stage 1
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Copiar archivos de configuración
# Nota: EasyPanel maneja Nginx, solo necesitamos el entrypoint y scripts de backend
COPY deploy/entrypoint.sh /app/entrypoint.sh
COPY deploy/start-backend.sh /app/start-backend.sh
COPY deploy/init-db.sh /app/init-db.sh

# Dar permisos de ejecución
RUN chmod +x /app/entrypoint.sh \
    && chmod +x /app/start-backend.sh \
    && chmod +x /app/init-db.sh

# Exponer puerto (EasyPanel configura el puerto, típicamente 80)
EXPOSE 80

# Health check (Flask sirve /health)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Usar entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando por defecto (Flask directamente, EasyPanel maneja Nginx)
CMD ["/app/start-backend.sh"]

