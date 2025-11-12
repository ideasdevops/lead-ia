#!/bin/bash
# No usar set -e aquí porque queremos continuar aunque falle la verificación de DB

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
    echo "⏳ Verificando conexión a PostgreSQL (contenedor externo)..."
    
    # Extraer host y puerto de DATABASE_URL usando Python para parsing más robusto
    # En EasyPanel, el host debe ser el nombre del servicio de PostgreSQL (ej: cloud_lead-ia-db)
    DB_INFO=$(python3 << 'PYTHON_SCRIPT'
import os
import re
import sys

url = os.environ.get('DATABASE_URL', '')
if not url:
    sys.exit(1)

# Formato: postgresql://user:pass@host:port/dbname
# O: postgresql://user:pass@host/dbname
match = re.search(r'@([^:/]+)(?::(\d+))?(?:/|$)', url)
if match:
    host = match.group(1)
    port = match.group(2) if match.group(2) else '5432'
    print(f'{host}:{port}')
    sys.exit(0)
else:
    sys.exit(1)
PYTHON_SCRIPT
)
    
    if [ $? -eq 0 ] && [ -n "$DB_INFO" ]; then
        DB_HOST=$(echo $DB_INFO | cut -d: -f1)
        DB_PORT=$(echo $DB_INFO | cut -d: -f2)
        
        # Verificar que no sea un placeholder o localhost
        # En producción, la DB debe estar en un contenedor externo
        if [ "$DB_HOST" != "host" ] && [ "$DB_HOST" != "localhost" ] && [ "$DB_HOST" != "127.0.0.1" ] && [ "$DB_HOST" != "postgres" ]; then
            MAX_RETRIES=5
            RETRY_COUNT=0
            echo "Intentando conectar a PostgreSQL en $DB_HOST:$DB_PORT..."
            
            while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
                if pg_isready -h "$DB_HOST" -p "$DB_PORT" -t 2 2>/dev/null; then
                    echo "✅ PostgreSQL disponible en $DB_HOST:$DB_PORT"
                    break
                fi
                RETRY_COUNT=$((RETRY_COUNT + 1))
                echo "Esperando PostgreSQL... (intento $RETRY_COUNT/$MAX_RETRIES)"
                sleep 3
            done
            
            if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
                echo "⚠️  ADVERTENCIA: No se pudo conectar a PostgreSQL después de $MAX_RETRIES intentos"
                echo "   Continuando de todas formas. La aplicación intentará conectarse al iniciar."
            fi
        else
            echo "ℹ️  Host de PostgreSQL parece ser un placeholder ($DB_HOST), omitiendo verificación"
        fi
    else
        echo "ℹ️  No se pudo parsear DATABASE_URL correctamente, omitiendo verificación"
    fi
else
    if [ "${SKIP_DB_CHECK:-false}" = "true" ]; then
        echo "ℹ️  Verificación de PostgreSQL deshabilitada (SKIP_DB_CHECK=true)"
    fi
fi

# Inicializar base de datos si es necesario
# Solo inicializar una vez para evitar recrear tablas en cada reinicio
if [ "$INIT_DB" = "true" ] && [ ! -f /app/database/.initialized ]; then
    echo "📦 Inicializando base de datos (primera vez)..."
    if /app/init-db.sh; then
        touch /app/database/.initialized
        echo "✅ Base de datos inicializada correctamente"
    else
        echo "⚠️  Error al inicializar base de datos, continuando..."
    fi
elif [ -f /app/database/.initialized ]; then
    echo "ℹ️  Base de datos ya inicializada (omitiendo init_db)"
fi

# Ejecutar comando pasado como argumento o supervisor por defecto
if [ "$#" -gt 0 ]; then
    exec "$@"
else
    echo "🎯 Iniciando Supervisor..."
    exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
fi

