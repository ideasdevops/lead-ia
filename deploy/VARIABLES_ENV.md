# 🔧 Variables de Entorno y Volúmenes - Lead-IA

## 📋 Variables de Entorno Requeridas

### Variables Obligatorias

```env
# Entorno de ejecución
FLASK_ENV=production

# Claves de seguridad (¡CAMBIAR EN PRODUCCIÓN!)
SECRET_KEY=tu-clave-secreta-muy-segura-aqui-cambiar
JWT_SECRET_KEY=tu-jwt-secret-key-muy-segura-aqui-cambiar

# Base de datos PostgreSQL
DATABASE_URL=postgresql://usuario:contraseña@host:5432/lead_ia

# CORS - Dominios permitidos
CORS_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com

# Inicialización de base de datos (solo primera vez)
INIT_DB=true
```

### Variables Opcionales

```env
# Puerto del backend (por defecto: 5000)
PORT=5000

# Configuración de JWT (opcional, tiene valores por defecto)
JWT_ACCESS_TOKEN_EXPIRES=86400  # 24 horas en segundos
JWT_REFRESH_TOKEN_EXPIRES=2592000  # 30 días en segundos
```

## 🔐 Generar Claves Secretas Seguras

### Opción 1: Python
```python
import secrets
print("SECRET_KEY=" + secrets.token_urlsafe(32))
print("JWT_SECRET_KEY=" + secrets.token_urlsafe(32))
```

### Opción 2: OpenSSL
```bash
openssl rand -hex 32  # Para SECRET_KEY
openssl rand -hex 32  # Para JWT_SECRET_KEY
```

### Opción 3: Online
- https://randomkeygen.com/
- Usar "CodeIgniter Encryption Keys" o "Fort Knox Passwords"

## 📦 Volúmenes Persistentes

### Volumen 1: Logs

| Propiedad | Valor |
|-----------|-------|
| **Nombre** | `lead-ia-logs` |
| **Ruta en Contenedor** | `/app/logs` |
| **Tamaño Recomendado** | 1GB |
| **Descripción** | Logs de aplicación, nginx y supervisor |
| **Tipo** | VOLUME |

**Contenido:**
- `/app/logs/nginx-access.log` - Logs de acceso de Nginx
- `/app/logs/nginx-error.log` - Logs de error de Nginx
- `/var/log/supervisor/` - Logs de Supervisor (backend, nginx)

### Volumen 2: Database (Datos Persistentes)

| Propiedad | Valor |
|-----------|-------|
| **Nombre** | `lead-ia-database` |
| **Ruta en Contenedor** | `/app/database` |
| **Tamaño Recomendado** | 10GB |
| **Descripción** | Archivos de inicialización y datos persistentes |
| **Tipo** | VOLUME |

**Contenido:**
- `/app/database/.initialized` - Flag de inicialización
- Archivos de backup (si se implementan)
- Datos temporales

## 📝 Ejemplo Completo de Configuración

### Variables de Entorno en EasyPanel

```env
FLASK_ENV=production
SECRET_KEY=aB3xY9mK2pL8qR5tV1wZ4cF7hJ0nM6sD9gH2jK5lP8qR1tV4wX7zA0bC3eF6
JWT_SECRET_KEY=mN9bV2cX5zA8dF1gH4jK7lP0qR3tV6wY9zB2cE5fH8jK1lM4nP7qR0tV
DATABASE_URL=postgresql://leaduser:SecurePass123!@postgres-host:5432/lead_ia
CORS_ORIGINS=https://lead-ia.tu-dominio.com,https://www.lead-ia.tu-dominio.com
INIT_DB=true
```

### Volúmenes en EasyPanel

```
Volumen 1:
  Nombre: lead-ia-logs
  Ruta: /app/logs
  Tamaño: 1GB

Volumen 2:
  Nombre: lead-ia-database
  Ruta: /app/database
  Tamaño: 10GB
```

## 🗄️ Configuración de PostgreSQL

### Opción 1: PostgreSQL en EasyPanel

1. Crear servicio PostgreSQL en EasyPanel
2. Obtener la URL de conexión automática
3. Usar esa URL en `DATABASE_URL`

**Ejemplo:**
```env
DATABASE_URL=postgresql://postgres:password123@postgres-service:5432/lead_ia
```

### Opción 2: PostgreSQL Externo

Si usas un servicio externo (AWS RDS, DigitalOcean, etc.):

**Formato de DATABASE_URL:**
```
postgresql://[usuario]:[contraseña]@[host]:[puerto]/[nombre_bd]
```

**Ejemplo AWS RDS:**
```env
DATABASE_URL=postgresql://admin:MySecurePass@lead-ia-db.xxxxx.us-east-1.rds.amazonaws.com:5432/lead_ia
```

**Ejemplo DigitalOcean:**
```env
DATABASE_URL=postgresql://doadmin:password@db-postgresql-nyc3-12345.db.ondigitalocean.com:25060/lead_ia?sslmode=require
```

## ⚠️ Importante: Seguridad

### ✅ Hacer:
- ✅ Generar claves secretas únicas y seguras
- ✅ Usar HTTPS en producción
- ✅ Configurar CORS solo con dominios permitidos
- ✅ Usar contraseñas fuertes para PostgreSQL
- ✅ Habilitar SSL/TLS para conexiones a PostgreSQL
- ✅ Cambiar credenciales del superadmin después del primer login

### ❌ No Hacer:
- ❌ Usar claves de ejemplo en producción
- ❌ Compartir variables de entorno públicamente
- ❌ Permitir CORS con `*` en producción
- ❌ Usar contraseñas débiles
- ❌ Exponer PostgreSQL sin autenticación

## 🔄 Después del Primer Deploy

Una vez que la aplicación esté funcionando:

1. **Cambiar INIT_DB a false** (opcional, para evitar reinicializaciones):
   ```env
   INIT_DB=false
   ```

2. **Cambiar credenciales del superadmin** desde el panel de administración

3. **Verificar logs** para asegurar que todo funciona correctamente

## 📊 Resumen Rápido

### Variables Mínimas Requeridas:
```
FLASK_ENV=production
SECRET_KEY=<generar-clave-segura>
JWT_SECRET_KEY=<generar-clave-segura>
DATABASE_URL=<url-postgresql>
CORS_ORIGINS=<tu-dominio>
INIT_DB=true
```

### Volúmenes Mínimos Requeridos:
```
/app/logs (1GB)
/app/database (10GB)
```

## 🧪 Verificar Configuración

Después de configurar, verificar:

1. **Health Check**: `curl https://tu-dominio.com/health`
2. **Variables cargadas**: Revisar logs del contenedor
3. **Conexión a BD**: Verificar logs del backend
4. **Volúmenes montados**: `docker exec <container> ls -la /app/logs`

