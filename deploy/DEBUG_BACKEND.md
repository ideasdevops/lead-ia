# 🐛 Debug del Backend - Lead-IA

## Problema: Backend se reinicia constantemente

Si el backend falla con `exit status 1` y se reinicia continuamente, sigue estos pasos:

### 1. Ver logs de error del backend

```bash
# Acceder al contenedor
docker exec -it <container-name> bash

# Ver logs de error
tail -f /var/log/supervisor/backend.err.log

# Ver logs de salida
tail -f /var/log/supervisor/backend.out.log

# Ver todos los logs de supervisor
tail -f /var/log/supervisor/supervisord.log
```

### 2. Verificar que el código esté actualizado

```bash
# Verificar que los archivos tengan los cambios recientes
docker exec -it <container-name> cat /app/backend/config.py | grep -A 5 "CRÍTICO"
docker exec -it <container-name> cat /app/backend/app/__init__.py | grep -A 5 "CONVERTIDO"
```

### 3. Verificar variables de entorno

```bash
docker exec -it <container-name> env | grep -E "DATABASE_URL|FLASK_ENV|SECRET_KEY"
```

### 4. Probar inicio manual del backend

```bash
docker exec -it <container-name> bash
cd /app/backend
python run.py
```

Esto mostrará el error exacto que está causando el fallo.

### 5. Verificar conversión de DATABASE_URL

```bash
docker exec -it <container-name> python3 -c "
import os
url = os.environ.get('DATABASE_URL', '')
print('DATABASE_URL:', url)
print('Usa postgresql://:', url.startswith('postgresql://'))
print('Usa postgres://:', url.startswith('postgres://'))
"
```

### 6. Verificar que psycopg2 esté instalado

```bash
docker exec -it <container-name> python3 -c "
try:
    import psycopg2
    print('✅ psycopg2 instalado:', psycopg2.__version__)
except ImportError as e:
    print('❌ psycopg2 NO instalado:', e)
"
```

### 7. Probar conexión a PostgreSQL

```bash
docker exec -it <container-name> python3 -c "
from sqlalchemy import create_engine
import os

url = os.environ.get('DATABASE_URL', '')
if url.startswith('postgres://'):
    url = url.replace('postgres://', 'postgresql://', 1)

try:
    engine = create_engine(url, connect_args={'connect_timeout': 5})
    print('✅ SQLAlchemy puede crear engine')
    conn = engine.connect()
    print('✅ Conexión a PostgreSQL exitosa')
    conn.close()
except Exception as e:
    print('❌ Error:', e)
    import traceback
    traceback.print_exc()
"
```

## Errores Comunes

### Error: `sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres`

**Causa:** La URL usa `postgres://` en lugar de `postgresql://`

**Solución:**
1. Verificar que `DATABASE_URL` use `postgresql://`
2. O verificar que el código de conversión esté funcionando

### Error: `ModuleNotFoundError: No module named 'psycopg2'`

**Causa:** `psycopg2-binary` no está instalado

**Solución:**
- Verificar que `requirements.txt` incluya `psycopg2-binary`
- Reconstruir el contenedor

### Error: `OperationalError: could not connect to server`

**Causa:** No se puede conectar a PostgreSQL

**Solución:**
- Verificar que el servicio de PostgreSQL esté ejecutándose
- Verificar que el hostname en `DATABASE_URL` sea correcto
- Verificar credenciales

### Error: `ValueError: DATABASE_URL no está configurada`

**Causa:** La variable de entorno no está definida

**Solución:**
- Agregar `DATABASE_URL` en las variables de entorno de EasyPanel

## Comandos Útiles

```bash
# Ver estado de supervisor
docker exec -it <container-name> supervisorctl status

# Reiniciar solo el backend
docker exec -it <container-name> supervisorctl restart backend

# Ver logs en tiempo real
docker logs <container-name> -f

# Ver últimas 100 líneas de logs
docker logs <container-name> --tail 100
```

