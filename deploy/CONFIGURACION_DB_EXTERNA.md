# 🗄️ Configuración de Base de Datos Externa - Lead-IA

## Arquitectura

En producción, la base de datos PostgreSQL está en un **contenedor separado** del contenedor de la aplicación. Esto permite:
- Escalabilidad independiente
- Mejor gestión de recursos
- Facilita backups y mantenimiento

## Configuración en EasyPanel

### 1. Servicio de Base de Datos

El servicio de PostgreSQL debe estar configurado como un servicio separado en EasyPanel:
- **Nombre del servicio:** `lead-ia-db` (o `cloud_lead-ia-db` dependiendo del proyecto)
- **Tipo:** PostgreSQL
- **Puerto interno:** 5432

### 2. Variable de Entorno DATABASE_URL

En el servicio de la aplicación (`lead-ia`), configurar `DATABASE_URL` con el **nombre del servicio de PostgreSQL** como hostname:

```env
DATABASE_URL=postgresql://usuario:contraseña@cloud_lead-ia-db:5432/leadia-db?sslmode=disable
```

**Importante:**
- ✅ Usar `postgresql://` (no `postgres://`) - SQLAlchemy lo requiere
- ✅ El hostname debe ser el **nombre del servicio** en EasyPanel (ej: `cloud_lead-ia-db`)
- ✅ En EasyPanel, los servicios se comunican usando el nombre del servicio como hostname
- ❌ NO usar `localhost` o `127.0.0.1` - la DB está en otro contenedor
- ❌ NO usar `postgres://` - SQLAlchemy no lo soporta

### 3. Formato de DATABASE_URL

```
postgresql://[usuario]:[contraseña]@[nombre-servicio-db]:[puerto]/[nombre-db]?[opciones]
```

**Ejemplo:**
```
postgresql://postgres:l3adia2k25@cloud_lead-ia-db:5432/leadia-db?sslmode=disable
```

**Componentes:**
- `postgresql://` - Esquema (requerido por SQLAlchemy)
- `postgres` - Usuario de PostgreSQL
- `l3adia2k25` - Contraseña
- `cloud_lead-ia-db` - **Nombre del servicio de PostgreSQL en EasyPanel**
- `5432` - Puerto (por defecto 5432)
- `leadia-db` - Nombre de la base de datos
- `?sslmode=disable` - Opciones (deshabilitar SSL en red interna)

## Verificación

### 1. Verificar que el servicio de DB existe

En EasyPanel, verificar que existe un servicio llamado `lead-ia-db` o `cloud_lead-ia-db`.

### 2. Verificar conectividad desde el contenedor de la app

```bash
# Acceder al contenedor de la aplicación
docker exec -it <container-name> bash

# Probar conexión a PostgreSQL
pg_isready -h cloud_lead-ia-db -p 5432

# Debe mostrar: cloud_lead-ia-db:5432 - accepting connections
```

### 3. Verificar logs de inicio

Al iniciar el contenedor, deberías ver:

```
⏳ Verificando conexión a PostgreSQL (contenedor externo)...
Intentando conectar a PostgreSQL en cloud_lead-ia-db:5432...
✅ PostgreSQL disponible en cloud_lead-ia-db:5432
```

## Troubleshooting

### Error: "host:5432 - no response"

**Causa:** El hostname en `DATABASE_URL` es incorrecto o es un placeholder.

**Solución:**
1. Verificar el nombre exacto del servicio de PostgreSQL en EasyPanel
2. Usar ese nombre exacto en `DATABASE_URL`
3. Asegurarse de que el servicio de PostgreSQL esté ejecutándose

### Error: "No se pudo parsear DATABASE_URL"

**Causa:** El formato de `DATABASE_URL` es incorrecto.

**Solución:**
- Verificar que use `postgresql://` (no `postgres://`)
- Verificar que el formato sea: `postgresql://user:pass@host:port/dbname`

### Error: "DATABASE_URL no está configurada"

**Causa:** La variable de entorno `DATABASE_URL` no está definida.

**Solución:**
- Agregar `DATABASE_URL` en las variables de entorno del servicio en EasyPanel
- Usar el formato correcto con el nombre del servicio como hostname

### Error: "Can't load plugin: sqlalchemy.dialects:postgres"

**Causa:** La URL usa `postgres://` en lugar de `postgresql://`.

**Solución:**
- Cambiar `postgres://` por `postgresql://` en `DATABASE_URL`
- El código también convierte automáticamente, pero es mejor usar el formato correcto desde el inicio

## Ejemplo Completo de Configuración

### En EasyPanel - Servicio `lead-ia-db`:
- **Tipo:** PostgreSQL
- **Puerto:** 5432
- **Base de datos:** `leadia-db`
- **Usuario:** `postgres`
- **Contraseña:** `l3adia2k25`

### En EasyPanel - Servicio `lead-ia` (aplicación):
**Variables de entorno:**
```env
DATABASE_URL=postgresql://postgres:l3adia2k25@cloud_lead-ia-db:5432/leadia-db?sslmode=disable
FLASK_ENV=production
SECRET_KEY=tu-secret-key
JWT_SECRET_KEY=tu-jwt-secret-key
CORS_ORIGINS=https://sumpetrol.com.ar,https://linkin.sumpetrol.com.ar
INIT_DB=true
```

## Notas Importantes

1. **Red de Docker:** En EasyPanel, los servicios en el mismo proyecto pueden comunicarse usando el nombre del servicio como hostname.

2. **Seguridad:** En producción, considera:
   - Usar contraseñas fuertes
   - Habilitar SSL si es necesario
   - Restringir acceso a la base de datos

3. **Backups:** Configura backups regulares del volumen de PostgreSQL en EasyPanel.

4. **Monitoreo:** Monitorea el uso de recursos de ambos servicios (app y DB) por separado.

