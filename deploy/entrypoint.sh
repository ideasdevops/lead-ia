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
    
    # Extraer host y puerto de DATABASE_URL
    # Formato: postgresql://user:pass@host:port/dbname
    DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
    DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
    
    # Si no se pudo extraer, intentar formato alternativo
    if [ -z "$DB_HOST" ]; then
        DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\).*/\1/p')
    fi
    if [ -z "$DB_PORT" ]; then
        DB_PORT=5432
    fi
    
    # Solo intentar conexión si tenemos host
    if [ -n "$DB_HOST" ] && [ "$DB_HOST" != "localhost" ] && [ "$DB_HOST" != "127.0.0.1" ]; then
        MAX_RETRIES=30
        RETRY_COUNT=0
        until pg_isready -h "$DB_HOST" -p "$DB_PORT" 2>/dev/null || [ $RETRY_COUNT -ge $MAX_RETRIES ]; do
            RETRY_COUNT=$((RETRY_COUNT + 1))
            echo "Esperando PostgreSQL en $DB_HOST:$DB_PORT... (intento $RETRY_COUNT/$MAX_RETRIES)"
            sleep 2
        done
        
        if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
            echo "⚠️  ADVERTENCIA: No se pudo conectar a PostgreSQL después de $MAX_RETRIES intentos"
            echo "   Continuando de todas formas..."
        else
            echo "✅ PostgreSQL disponible en $DB_HOST:$DB_PORT"
        fi
    else
        echo "ℹ️  PostgreSQL local o no especificado, omitiendo verificación"
    fi
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

