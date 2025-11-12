# ✅ Checklist de Deploy - Lead-IA

## 📋 Pre-Deploy

### Repositorio
- [ ] Código en GitHub (`git@github.com:ideasdevops/lead-ia.git`)
- [ ] Branch `main` actualizado
- [ ] Dockerfile configurado
- [ ] Archivos de deploy en `/deploy`
- [ ] `.dockerignore` configurado

### Archivos de Configuración
- [x] `Dockerfile` - Multi-stage build (Frontend + Backend)
- [x] `deploy/supervisor.conf` - Gestión de procesos
- [x] `deploy/nginx.conf` - Reverse proxy
- [x] `deploy/entrypoint.sh` - Inicialización
- [x] `deploy/start-backend.sh` - Inicio Flask
- [x] `deploy/init-db.sh` - Inicialización BD
- [x] `deploy/easypanel.json` - Config EasyPanel
- [x] `.dockerignore` - Archivos excluidos
- [x] `docker-compose.yml` - Para desarrollo local

## 🔧 Configuración en EasyPanel

### 1. Crear Aplicación
- [ ] Tipo: **Docker**
- [ ] Repositorio: `git@github.com:ideasdevops/lead-ia.git`
- [ ] Branch: `main`
- [ ] Dockerfile: `Dockerfile`
- [ ] Context: `.`

### 2. Variables de Entorno
```env
FLASK_ENV=production
SECRET_KEY=<generar-clave-segura-aleatoria>
JWT_SECRET_KEY=<generar-clave-segura-aleatoria>
DATABASE_URL=postgresql://usuario:contraseña@host:5432/lead_ia
CORS_ORIGINS=https://tu-dominio.com
INIT_DB=true
```

⚠️ **IMPORTANTE**: 
- [ ] Cambiar `SECRET_KEY` por una clave segura
- [ ] Cambiar `JWT_SECRET_KEY` por una clave segura
- [ ] Configurar `DATABASE_URL` correctamente
- [ ] Configurar `CORS_ORIGINS` con dominio de producción

### 3. Volúmenes
- [ ] `/app/logs` - 1GB (Logs de aplicación)
- [ ] `/app/database` - 10GB (Datos persistentes)

### 4. Puertos
- [ ] Puerto público: `80`
- [ ] Protocolo: `HTTP`

### 5. Health Check
- [ ] Path: `/health`
- [ ] Interval: `30s`
- [ ] Timeout: `10s`
- [ ] Start Period: `40s`
- [ ] Retries: `3`

### 6. Recursos
- [ ] Memory: Mínimo 1GB (recomendado 2GB)
- [ ] CPU: Mínimo 1 CPU (recomendado 2 CPU)
- [ ] Restart Policy: `Always`

## 🗄️ Base de Datos PostgreSQL

### Opción 1: PostgreSQL en EasyPanel
- [ ] Crear servicio PostgreSQL en EasyPanel
- [ ] Obtener URL de conexión
- [ ] Configurar en `DATABASE_URL`

### Opción 2: PostgreSQL Externo
- [ ] Crear instancia PostgreSQL (AWS RDS, DigitalOcean, etc.)
- [ ] Configurar acceso desde EasyPanel
- [ ] Configurar en `DATABASE_URL`

## 🚀 Post-Deploy

### Verificación Inicial
- [ ] Health check responde: `https://tu-dominio.com/health`
- [ ] Frontend carga: `https://tu-dominio.com`
- [ ] Login funciona con credenciales:
  - Email: `devops@ideasdevops.com`
  - Password: `s3rv3rfa1l`

### Verificación de Servicios
- [ ] Flask corriendo (puerto 5000)
- [ ] Nginx corriendo (puerto 80)
- [ ] Supervisor gestionando procesos
- [ ] Base de datos inicializada

### Verificación de Funcionalidades
- [ ] Dashboard carga correctamente
- [ ] Búsqueda de leads funciona
- [ ] Resultados se muestran correctamente
- [ ] Gestión de usuarios funciona
- [ ] Gestión de roles funciona
- [ ] Exportación a CSV funciona

### Verificación de Logs
- [ ] Logs de backend accesibles: `/app/logs`
- [ ] Logs de nginx accesibles: `/var/log/supervisor/nginx.out.log`
- [ ] No hay errores críticos en los logs

## 🔒 Seguridad

- [ ] Variables de entorno con claves seguras
- [ ] CORS configurado correctamente
- [ ] HTTPS configurado (si aplica)
- [ ] Firewall configurado
- [ ] Backups de base de datos programados

## 📊 Monitoreo

- [ ] Health checks funcionando
- [ ] Logs siendo monitoreados
- [ ] Alertas configuradas (si aplica)
- [ ] Métricas de rendimiento (si aplica)

## ✅ Finalización

- [ ] Documentación actualizada
- [ ] Equipo notificado del deploy
- [ ] Credenciales compartidas de forma segura
- [ ] Acceso de prueba verificado

