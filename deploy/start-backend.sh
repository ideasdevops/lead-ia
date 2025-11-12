#!/bin/bash
set -e

cd /app/backend

# Activar entorno virtual si existe (no necesario en Docker)
# source /app/venv/bin/activate

# Ejecutar Flask
echo "🚀 Iniciando servidor Flask..."
exec python run.py

