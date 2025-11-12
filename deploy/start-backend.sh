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
echo "📦 PORT configurado: ${PORT:-5000} (Flask debe usar 5000, Nginx usa 80)"

# Asegurar que PORT sea 5000 (no 80 que es para Nginx)
export PORT=5000

# Ejecutar con captura de errores
python run.py 2>&1 || {
    echo "❌ ERROR: Flask falló al iniciar"
    echo "📋 Últimos errores:"
    exit 1
}

