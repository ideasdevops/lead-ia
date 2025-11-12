#!/bin/bash
set -e

echo "🚀 Iniciando Lead-IA..."

# Crear directorios si no existen
mkdir -p /app/logs
mkdir -p /app/database
mkdir -p /var/log/supervisor

# Configurar permisos
chmod -R 755 /app/logs
chmod -R 755 /app/database

# Esperar a que PostgreSQL esté disponible (si se usa)
if [ -n "$DATABASE_URL" ]; then
    echo "⏳ Esperando conexión a PostgreSQL..."
    until pg_isready -h $(echo $DATABASE_URL | sed -e 's/.*@\(.*\):.*/\1/') -p $(echo $DATABASE_URL | sed -e 's/.*:\([0-9]*\).*/\1/') 2>/dev/null; do
        echo "Esperando PostgreSQL..."
        sleep 2
    done
    echo "✅ PostgreSQL disponible"
fi

# Inicializar base de datos si es necesario
if [ "$INIT_DB" = "true" ] || [ ! -f /app/database/.initialized ]; then
    echo "📦 Inicializando base de datos..."
    /app/init-db.sh
    touch /app/database/.initialized
    echo "✅ Base de datos inicializada"
fi

# Ejecutar comando pasado como argumento o supervisor por defecto
if [ "$#" -gt 0 ]; then
    exec "$@"
else
    echo "🎯 Iniciando Supervisor..."
    exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
fi

