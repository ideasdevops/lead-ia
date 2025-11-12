# 🔧 Troubleshooting - Lead-IA

## Problema: Sistema queda esperando PostgreSQL

### Síntoma
El contenedor queda en un loop infinito esperando PostgreSQL:
```
Esperando PostgreSQL...
host:5432 - no response
```

### Causas Posibles

1. **DATABASE_URL con placeholder**: Si `DATABASE_URL` contiene `host` literal en lugar de un host real
2. **PostgreSQL no accesible**: El host de PostgreSQL no es accesible desde el contenedor
3. **Parsing incorrecto**: El script no puede extraer correctamente el host y puerto

### Soluciones

#### Opción 1: Deshabilitar verificación de PostgreSQL

Agregar variable de entorno:
```env
SKIP_DB_CHECK=true
```

Esto hará que el contenedor inicie sin esperar PostgreSQL. La aplicación intentará conectarse cuando sea necesario.

#### Opción 2: Verificar DATABASE_URL

Asegúrate de que `DATABASE_URL` tenga el formato correcto:
```env
DATABASE_URL=postgresql://usuario:contraseña@host-real:5432/lead_ia
```

**NO usar:**
```env
DATABASE_URL=postgresql://usuario:contraseña@host:5432/lead_ia  # ❌ "host" es placeholder
```

#### Opción 3: Usar PostgreSQL en EasyPanel

1. Crear servicio PostgreSQL en EasyPanel
2. Obtener la URL de conexión automática
3. Usar esa URL en `DATABASE_URL`

### Verificación

Para verificar que PostgreSQL es accesible:

```bash
# Desde el contenedor
docker exec -it <container-name> bash
pg_isready -h <host> -p 5432
```

## Otros Problemas Comunes

### Error: No se puede conectar a PostgreSQL

**Solución:**
- Verificar que PostgreSQL esté ejecutándose
- Verificar firewall/red
- Verificar credenciales en `DATABASE_URL`
- Verificar que el host sea accesible desde el contenedor

### Error: Frontend no carga

**Solución:**
- Verificar logs: `docker logs <container-name>`
- Verificar que el build del frontend se completó
- Verificar logs de nginx: `/var/log/supervisor/nginx.err.log`

### Error: Backend no responde

**Solución:**
- Verificar logs del backend: `/var/log/supervisor/backend.err.log`
- Verificar que Flask esté corriendo
- Verificar variables de entorno

### Error: Health check falla

**Solución:**
- Verificar que nginx esté corriendo
- Verificar que el endpoint `/health` esté accesible
- Verificar logs de nginx

## Variables de Entorno Útiles

```env
# Deshabilitar verificación de PostgreSQL
SKIP_DB_CHECK=true

# Deshabilitar inicialización automática de BD
INIT_DB=false

# Modo debug (más logs)
FLASK_ENV=development
```

## Comandos de Diagnóstico

```bash
# Ver logs del contenedor
docker logs <container-name> -f

# Acceder al contenedor
docker exec -it <container-name> bash

# Ver estado de supervisor
docker exec -it <container-name> supervisorctl status

# Ver logs de nginx
docker exec -it <container-name> tail -f /var/log/supervisor/nginx.out.log

# Ver logs del backend
docker exec -it <container-name> tail -f /var/log/supervisor/backend.out.log

# Probar conexión a PostgreSQL
docker exec -it <container-name> pg_isready -h <host> -p 5432
```

