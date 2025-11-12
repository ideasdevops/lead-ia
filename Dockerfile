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
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorios necesarios
RUN mkdir -p /app/backend \
    /app/frontend/dist \
    /app/logs \
    /app/database \
    /var/log/supervisor \
    /etc/supervisor/conf.d \
    /etc/nginx/sites-available

WORKDIR /app

# Copiar requirements del backend
COPY backend/requirements.txt /app/backend/
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Instalar py_lead_generation (copiar setup.py también)
COPY py_lead_generation/ /app/py_lead_generation/
COPY setup.py /app/
RUN pip install --no-cache-dir -e /app/

# Copiar código del backend
COPY backend/ /app/backend/

# Copiar frontend construido desde stage 1
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Copiar archivos de configuración
COPY deploy/nginx.conf /etc/nginx/sites-available/default
COPY deploy/supervisor.conf /etc/supervisor/conf.d/supervisord.conf
COPY deploy/entrypoint.sh /app/entrypoint.sh
COPY deploy/start-backend.sh /app/start-backend.sh
COPY deploy/init-db.sh /app/init-db.sh

# Dar permisos de ejecución
RUN chmod +x /app/entrypoint.sh \
    && chmod +x /app/start-backend.sh \
    && chmod +x /app/init-db.sh

# Exponer puerto 80
EXPOSE 80

# Health check (nginx sirve /health)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Usar entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando por defecto (supervisor)
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

