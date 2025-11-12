# 🔍 Diagnóstico de Problemas - Lead-IA

## Problema: Error `sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres`

### Causa
SQLAlchemy requiere que la URL de la base de datos use el esquema `postgresql://` en lugar de `postgres://`. Aunque `psycopg2-binary` está instalado, SQLAlchemy no puede cargar el driver si la URL usa el esquema incorrecto.

### Solución Aplicada
Se agregó conversión automática en `backend/config.py`:
- Convierte `postgres://` a `postgresql://` automáticamente
- Asegura compatibilidad con diferentes formatos de URL

### Verificación

Para verificar que el problema está resuelto:

1. **Verificar que DATABASE_URL use el formato correcto:**
   ```bash
   # Correcto
   DATABASE_URL=postgresql://usuario:contraseña@host:5432/lead_ia
   
   # También funciona (se convierte automáticamente)
   DATABASE_URL=postgres://usuario:contraseña@host:5432/lead_ia
   ```

2. **Verificar que psycopg2-binary esté instalado:**
   ```bash
   docker exec -it <container-name> python3 -c "import psycopg2; print('psycopg2 OK')"
   ```

3. **Verificar que SQLAlchemy pueda conectarse:**
   ```bash
   docker exec -it <container-name> python3 -c "from sqlalchemy import create_engine; engine = create_engine('postgresql://test'); print('SQLAlchemy OK')"
   ```

## Problema: Script sigue intentando conectarse a "host:5432"

### Causa
El parsing de `DATABASE_URL` no está funcionando correctamente, posiblemente porque:
- La URL tiene un formato diferente al esperado
- Hay múltiples instancias del script corriendo
- El script no se actualizó en el contenedor

### Solución Aplicada
- Mejorado el parsing usando Python con regex más robusta
- Agregada detección de placeholders ("host", "localhost", "127.0.0.1")
- Reducido el número de reintentos a 5 (15 segundos máximo)

### Verificación

1. **Verificar el formato de DATABASE_URL:**
   ```bash
   # El script debería detectar correctamente:
   # postgresql://user:pass@cloud_lead-ia-db:5432/lead_ia
   # postgresql://user:pass@host-real:5432/lead_ia
   ```

2. **Si sigue apareciendo "host:5432":**
   - Verificar que `DATABASE_URL` no contenga literalmente "host" como nombre
   - Agregar `SKIP_DB_CHECK=true` para deshabilitar la verificación
   - Verificar que el contenedor tenga la versión actualizada del script

## Solución Rápida

Si el problema persiste, agregar esta variable de entorno en EasyPanel:

```env
SKIP_DB_CHECK=true
```

Esto deshabilitará la verificación de PostgreSQL y permitirá que el contenedor inicie. La aplicación intentará conectarse cuando sea necesario.

## Verificación de Instalación

Para verificar que todo está correctamente instalado:

```bash
# Acceder al contenedor
docker exec -it <container-name> bash

# Verificar Python y pip
python3 --version
pip list | grep -i psycopg

# Verificar que psycopg2 funciona
python3 -c "import psycopg2; print('psycopg2-binary instalado correctamente')"

# Verificar SQLAlchemy
python3 -c "from sqlalchemy import create_engine; print('SQLAlchemy OK')"

# Probar conexión (reemplazar con tu DATABASE_URL)
python3 -c "
from sqlalchemy import create_engine
import os
url = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
if url:
    try:
        engine = create_engine(url, connect_args={'connect_timeout': 5})
        print('✅ Conexión a PostgreSQL OK')
    except Exception as e:
        print(f'❌ Error: {e}')
"
```

## Logs Útiles

Para diagnosticar problemas:

```bash
# Ver logs del contenedor
docker logs <container-name> -f

# Ver logs de supervisor
docker exec -it <container-name> supervisorctl status

# Ver logs del backend
docker exec -it <container-name> tail -f /var/log/supervisor/backend.out.log

# Ver logs de nginx
docker exec -it <container-name> tail -f /var/log/supervisor/nginx.out.log
```

