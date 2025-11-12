# 🚀 Guía de Deploy - Lead-IA con EasyPanel

## 📋 Resumen

Esta guía explica cómo desplegar Lead-IA en producción usando EasyPanel con Docker.

## 🏗️ Arquitectura

```
┌─────────────────────────────────────┐
│         EasyPanel / Docker          │
│                                     │
│  ┌──────────────────────────────┐ │
│  │      Supervisor (PID 1)       │ │
│  │                                │ │
│  │  ┌──────────┐  ┌──────────┐  │ │
│  │  │  Flask   │  │  Nginx    │  │ │
│  │  │  :5000   │  │  :80      │  │ │
│  │  └──────────┘  └──────────┘  │ │
│  └──────────────────────────────┘ │
│                                     │
│  ┌──────────────────────────────┐ │
│  │     Volúmenes Persistentes    │ │
│  │  - /app/logs                  │ │
│  │  - /app/database              │ │
│  └──────────────────────────────┘ │
└─────────────────────────────────────┘
```

## 📦 Componentes del Deploy

### 1. Dockerfile
- **Multi-stage build**: Frontend (Node.js) + Backend (Python)
- **Base**: `python:3.10-slim` con Nginx y Supervisor
- **Puertos**: 80 (Nginx)
- **Volúmenes**: `/app/logs`, `/app/database`

### 2. Supervisor
- Gestiona Flask (backend) y Nginx como servicios
- Reinicio automático si falla algún proceso
- Logs centralizados en `/var/log/supervisor/`

### 3. Nginx
- Sirve archivos estáticos del frontend (React build)
- Proxy reverso a Flask para `/api`
- Healthcheck endpoint en `/health`

### 4. Scripts
- `entrypoint.sh`: Inicialización del contenedor
- `start-backend.sh`: Inicio del servidor Flask
- `init-db.sh`: Inicialización de base de datos

## 🔧 Configuración en EasyPanel

### Paso 1: Crear Aplicación

1. Ir a EasyPanel Dashboard
2. Crear nueva aplicación
3. Seleccionar **"Docker"** como tipo
4. Conectar repositorio: `git@github.com:ideasdevops/lead-ia.git`
5. Branch: `main`

### Paso 2: Configurar Build

- **Dockerfile Path**: `Dockerfile` (raíz)
- **Build Context**: `.` (raíz)
- **Build Command**: (vacío, se usa Dockerfile)

### Paso 3: Variables de Entorno

```env
FLASK_ENV=production
SECRET_KEY=tu-clave-secreta-muy-segura-aqui-cambiar
JWT_SECRET_KEY=tu-jwt-secret-key-muy-segura-aqui-cambiar
DATABASE_URL=postgresql://usuario:contraseña@host:5432/lead_ia
CORS_ORIGINS=https://tu-dominio.com
INIT_DB=true
```

⚠️ **IMPORTANTE**: 
- Cambiar `SECRET_KEY` y `JWT_SECRET_KEY` por claves seguras en producción
- Configurar `DATABASE_URL` con tus credenciales de PostgreSQL
- Ajustar `CORS_ORIGINS` con tu dominio de producción

### Paso 4: Volúmenes Persistentes

Añadir estos volúmenes:

| Ruta | Tamaño | Descripción |
|------|--------|-------------|
| `/app/logs` | 1GB | Logs de aplicación, nginx y supervisor |
| `/app/database` | 10GB | Datos persistentes y archivos de inicialización |

### Paso 5: Puertos

- **Puerto del contenedor**: `80`
- **Protocolo**: HTTP
- **Exponer**: Sí

### Paso 6: Health Check

- **Path**: `/health`
- **Interval**: 30 segundos
- **Timeout**: 10 segundos
- **Start Period**: 40 segundos
- **Retries**: 3

### Paso 7: Configuración Adicional

- **Restart Policy**: Always
- **Memory Limit**: Mínimo 1GB (recomendado 2GB)
- **CPU Limit**: Mínimo 1 CPU (recomendado 2 CPU)

## 🚀 Proceso de Deploy

1. **Build**: EasyPanel construye la imagen Docker (multi-stage)
2. **Inicialización**: `entrypoint.sh` ejecuta:
   - Crea directorios necesarios
   - Espera conexión a PostgreSQL
   - Inicializa base de datos si `INIT_DB=true`
   - Configura permisos
3. **Supervisor**: Inicia Flask (backend) y Nginx
4. **Health Check**: Verifica que `/health` responde
5. **Listo**: Aplicación disponible en el dominio configurado

## 📊 Base de Datos PostgreSQL

### Opción 1: PostgreSQL en EasyPanel

1. Crear servicio PostgreSQL en EasyPanel
2. Obtener la URL de conexión
3. Usar esa URL en `DATABASE_URL`

### Opción 2: PostgreSQL Externo

Usar un servicio PostgreSQL externo (AWS RDS, DigitalOcean, etc.) y configurar la URL en `DATABASE_URL`.

## ✅ Verificación Post-Deploy

### 1. Health Check
```bash
curl https://tu-dominio.com/health
# Debe retornar: {"status": "healthy"}
```

### 2. Frontend
- Abrir `https://tu-dominio.com`
- Debe cargar la aplicación React

### 3. Backend API
```bash
curl https://tu-dominio.com/api/dashboard/stats
# Debe retornar error 401 (requiere autenticación, esto es correcto)
```

### 4. Login
- Ir a `https://tu-dominio.com/login`
- Login con:
  - Email: `devops@ideasdevops.com`
  - Contraseña: `s3rv3rfa1l`

### 5. Verificación de Servicios

Conectarse al contenedor y verificar:
```bash
# Ver procesos de supervisor
supervisorctl status

# Ver logs
tail -f /var/log/supervisor/backend.out.log
tail -f /var/log/supervisor/nginx.out.log
```

## 🔍 Troubleshooting

### Error: No se puede conectar a PostgreSQL
- Verificar que `DATABASE_URL` sea correcta
- Verificar que PostgreSQL esté accesible desde el contenedor
- Verificar firewall/red

### Error: Frontend no carga
- Verificar que el build del frontend se haya completado
- Verificar logs de nginx: `/var/log/supervisor/nginx.err.log`
- Verificar que `/app/frontend/dist` contenga archivos

### Error: Backend no responde
- Verificar logs del backend: `/var/log/supervisor/backend.err.log`
- Verificar que Flask esté corriendo en puerto 5000
- Verificar variables de entorno

### Error: Health check falla
- Verificar que nginx esté corriendo
- Verificar que el endpoint `/health` esté accesible
- Verificar logs de nginx

## 📝 Notas Importantes

1. **Primera ejecución**: `INIT_DB=true` crea el superadmin automáticamente
2. **Seguridad**: Cambiar todas las claves secretas en producción
3. **CORS**: Configurar `CORS_ORIGINS` con el dominio de producción
4. **Logs**: Los logs se guardan en `/app/logs` (volumen persistente)
5. **Base de datos**: Asegurar backups regulares de PostgreSQL

## 🔄 Actualizaciones

Para actualizar la aplicación:
1. Hacer push a la rama `main` en GitHub
2. EasyPanel detectará los cambios
3. Reconstruirá la imagen automáticamente
4. Desplegará la nueva versión

## 📚 Recursos Adicionales

- [Documentación EasyPanel](https://easypanel.io/docs)
- [Docker Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Supervisor Documentation](http://supervisord.org/)

