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

# Esperar a que PostgreSQL esté disponible (si se usa y está habilitado)
if [ -n "$DATABASE_URL" ] && [ "${SKIP_DB_CHECK:-false}" != "true" ]; then
    echo "⏳ Verificando conexión a PostgreSQL..."
    
    # Extraer host y puerto de DATABASE_URL usando Python para parsing más robusto
    DB_INFO=$(python3 -c "
import os
import re
url = os.environ.get('DATABASE_URL', '')
if url:
    # Formato: postgresql://user:pass@host:port/dbname
    match = re.search(r'@([^:]+):(\d+)', url)
    if match:
        print(f'{match.group(1)}:{match.group(2)}')
    else:
        # Intentar sin puerto explícito
        match = re.search(r'@([^/]+)', url)
        if match:
            print(f'{match.group(1)}:5432')
" 2>/dev/null || echo "")
    
    if [ -n "$DB_INFO" ]; then
        DB_HOST=$(echo $DB_INFO | cut -d: -f1)
        DB_PORT=$(echo $DB_INFO | cut -d: -f2)
        
        # Verificar que no sea un placeholder
        if [ "$DB_HOST" != "host" ] && [ "$DB_HOST" != "localhost" ] && [ "$DB_HOST" != "127.0.0.1" ]; then
            MAX_RETRIES=10
            RETRY_COUNT=0
            echo "Intentando conectar a PostgreSQL en $DB_HOST:$DB_PORT..."
            
            until pg_isready -h "$DB_HOST" -p "$DB_PORT" -t 2 2>/dev/null || [ $RETRY_COUNT -ge $MAX_RETRIES ]; do
                RETRY_COUNT=$((RETRY_COUNT + 1))
                echo "Esperando PostgreSQL... (intento $RETRY_COUNT/$MAX_RETRIES)"
                sleep 3
            done
            
            if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
                echo "⚠️  ADVERTENCIA: No se pudo conectar a PostgreSQL después de $MAX_RETRIES intentos"
                echo "   Continuando de todas formas. La aplicación intentará conectarse al iniciar."
            else
                echo "✅ PostgreSQL disponible en $DB_HOST:$DB_PORT"
            fi
        else
            echo "ℹ️  Host de PostgreSQL parece ser un placeholder, omitiendo verificación"
        fi
    else
        echo "ℹ️  No se pudo parsear DATABASE_URL, omitiendo verificación"
    fi
else
    if [ "${SKIP_DB_CHECK:-false}" = "true" ]; then
        echo "ℹ️  Verificación de PostgreSQL deshabilitada (SKIP_DB_CHECK=true)"
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

