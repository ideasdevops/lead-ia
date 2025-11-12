# ⚙️ Configuración Completa para EasyPanel - Lead-IA

## 📋 Resumen de Configuración

Este documento contiene toda la configuración necesaria para desplegar Lead-IA en EasyPanel.

---

## 🔧 Variables de Entorno

### Copiar y Pegar en EasyPanel

```env
FLASK_ENV=production
SECRET_KEY=REEMPLAZAR_CON_CLAVE_SEGURA_DE_32_CARACTERES
JWT_SECRET_KEY=REEMPLAZAR_CON_CLAVE_SEGURA_DE_32_CARACTERES
DATABASE_URL=postgresql://usuario:contraseña@host:5432/lead_ia
CORS_ORIGINS=https://tu-dominio.com
INIT_DB=true
```

### 🔐 Generar Claves (Ejecutar en terminal)

```bash
# Generar SECRET_KEY
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"

# Generar JWT_SECRET_KEY
python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

**Ejemplo de salida:**
```
SECRET_KEY=K8mN2pQ5rT9vW1xY4zA7bC0dE3fG6hI9jK2lM5nP8qR1tV4wX7zA0bC3eF6
JWT_SECRET_KEY=mN9bV2cX5zA8dF1gH4jK7lP0qR3tV6wY9zB2cE5fH8jK1lM4nP7qR0tV
```

---

## 📦 Volúmenes Persistentes

### Volumen 1: Logs

```
Tipo: VOLUME
Nombre: lead-ia-logs
Ruta en Contenedor: /app/logs
Tamaño: 1GB
Descripción: Logs de aplicación, nginx y supervisor
```

### Volumen 2: Database

```
Tipo: VOLUME
Nombre: lead-ia-database
Ruta en Contenedor: /app/database
Tamaño: 10GB
Descripción: Datos persistentes y archivos de inicialización
```

---

## 🌐 Configuración de Puerto

```
Puerto del Contenedor: 80
Protocolo: HTTP
Exponer: Sí
```

---

## ❤️ Health Check

```
Path: /health
Interval: 30 segundos
Timeout: 10 segundos
Start Period: 40 segundos
Retries: 3
```

---

## 💻 Recursos del Contenedor

```
Memoria: 1GB (mínimo) / 2GB (recomendado)
CPU: 1 CPU (mínimo) / 2 CPU (recomendado)
Restart Policy: Always
```

---

## 🗄️ Configuración de PostgreSQL

### Si usas PostgreSQL en EasyPanel:

1. Crear servicio PostgreSQL
2. Obtener la URL de conexión automática
3. Usar esa URL en `DATABASE_URL`

**Ejemplo:**
```env
DATABASE_URL=postgresql://postgres:password@postgres-service:5432/lead_ia
```

### Si usas PostgreSQL externo:

**Formato:**
```env
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_bd
```

**Ejemplo AWS RDS:**
```env
DATABASE_URL=postgresql://admin:Pass123!@lead-ia-db.xxxxx.us-east-1.rds.amazonaws.com:5432/lead_ia
```

---

## 📝 Checklist de Configuración

### Paso 1: Crear Aplicación
- [ ] Tipo: **Docker**
- [ ] Repositorio: `git@github.com:ideasdevops/lead-ia.git`
- [ ] Branch: `main`
- [ ] Dockerfile: `Dockerfile`
- [ ] Context: `.`

### Paso 2: Variables de Entorno
- [ ] `FLASK_ENV=production`
- [ ] `SECRET_KEY` (generada y configurada)
- [ ] `JWT_SECRET_KEY` (generada y configurada)
- [ ] `DATABASE_URL` (configurada con PostgreSQL)
- [ ] `CORS_ORIGINS` (configurado con tu dominio)
- [ ] `INIT_DB=true` (solo primera vez)

### Paso 3: Volúmenes
- [ ] `/app/logs` (1GB)
- [ ] `/app/database` (10GB)

### Paso 4: Puerto
- [ ] Puerto: `80`
- [ ] Protocolo: `HTTP`
- [ ] Exponer: `Sí`

### Paso 5: Health Check
- [ ] Path: `/health`
- [ ] Interval: `30s`
- [ ] Timeout: `10s`
- [ ] Start Period: `40s`
- [ ] Retries: `3`

### Paso 6: Recursos
- [ ] Memoria: `1GB` o más
- [ ] CPU: `1` o más
- [ ] Restart Policy: `Always`

---

## ✅ Verificación Post-Deploy

### 1. Health Check
```bash
curl https://tu-dominio.com/health
# Debe retornar: {"status": "healthy"}
```

### 2. Frontend
- Abrir: `https://tu-dominio.com`
- Debe cargar la aplicación React

### 3. Login
- Email: `devops@ideasdevops.com`
- Contraseña: `s3rv3rfa1l`

### 4. Verificar Logs
En EasyPanel, verificar que no hay errores en los logs del contenedor.

---

## 🔄 Después del Primer Deploy Exitoso

1. **Cambiar INIT_DB** (opcional):
   ```env
   INIT_DB=false
   ```

2. **Cambiar credenciales del superadmin** desde el panel de administración

3. **Configurar dominio personalizado** (si aplica)

4. **Configurar SSL/HTTPS** (recomendado)

---

## 🆘 Troubleshooting

### Error: No se puede conectar a PostgreSQL
- Verificar que `DATABASE_URL` sea correcta
- Verificar que PostgreSQL esté accesible
- Verificar firewall/red

### Error: Health check falla
- Verificar que nginx esté corriendo
- Verificar logs: `/var/log/supervisor/nginx.err.log`

### Error: Frontend no carga
- Verificar que el build se completó
- Verificar logs de nginx

---

## 📞 Soporte

Para más información, consultar:
- [DEPLOY_EASYPANEL.md](../DEPLOY_EASYPANEL.md) - Guía completa
- [VARIABLES_ENV.md](./VARIABLES_ENV.md) - Detalles de variables
- [CHECKLIST_DEPLOY.md](./CHECKLIST_DEPLOY.md) - Checklist completo

