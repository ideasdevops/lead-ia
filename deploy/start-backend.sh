#!/bin/bash
# No usar set -e para capturar errores

cd /app/backend

# Activar entorno virtual si existe (no necesario en Docker)
# source /app/venv/bin/activate

# Ejecutar Flask con manejo de errores
echo "🚀 Iniciando servidor Flask..."
echo "📦 Directorio actual: $(pwd)"
echo "📦 Python: $(python --version)"
echo "📦 DATABASE_URL configurada: $(if [ -n "$DATABASE_URL" ]; then echo "Sí"; else echo "No"; fi)"

# Ejecutar con captura de errores
python run.py 2>&1 || {
    echo "❌ ERROR: Flask falló al iniciar"
    echo "📋 Últimos errores:"
    exit 1
}

