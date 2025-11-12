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
echo "📦 PORT configurado: ${PORT:-80} (EasyPanel maneja Nginx automáticamente)"

# Ejecutar con captura de errores y logging detallado
# Redirigir stderr a stdout para que supervisor capture todo
exec python run.py 2>&1

