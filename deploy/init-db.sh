#!/bin/bash
set -e

cd /app/backend

echo "📦 Inicializando base de datos..."

# Verificar que DATABASE_URL esté configurada
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  ADVERTENCIA: DATABASE_URL no está configurada"
    echo "   La base de datos no se inicializará automáticamente"
    exit 0
fi

# Ejecutar script de inicialización de Python
python init_db.py

echo "✅ Base de datos inicializada correctamente"

