# 🚀 Guía Rápida de Deploy - Lead-IA

## Desarrollo Local con Docker Compose

### Requisitos
- Docker
- Docker Compose

### Inicio Rápido

```bash
# Construir imágenes
make build

# Iniciar servicios
make up

# Ver logs
make logs

# Inicializar base de datos
make init-db
```

La aplicación estará disponible en:
- Frontend: http://localhost
- Backend API: http://localhost/api
- Health Check: http://localhost/health

### Comandos Útiles

```bash
# Acceder al shell del contenedor
make shell

# Ver estado de supervisor
make supervisor-status

# Reiniciar servicios
make restart

# Detener servicios
make down

# Limpiar todo (incluye volúmenes)
make clean
```

## Deploy en EasyPanel

Ver la guía completa en [DEPLOY_EASYPANEL.md](DEPLOY_EASYPANEL.md)

### Pasos Rápidos

1. **Crear aplicación en EasyPanel**
   - Tipo: Docker
   - Repositorio: `git@github.com:ideasdevops/lead-ia.git`
   - Branch: `main`

2. **Configurar variables de entorno**
   ```env
   FLASK_ENV=production
   SECRET_KEY=<clave-segura>
   JWT_SECRET_KEY=<clave-segura>
   DATABASE_URL=postgresql://user:pass@host:5432/lead_ia
   CORS_ORIGINS=https://tu-dominio.com
   INIT_DB=true
   ```

3. **Configurar volúmenes**
   - `/app/logs` (1GB)
   - `/app/database` (10GB)

4. **Configurar puerto**
   - Puerto: `80`
   - Protocolo: `HTTP`

5. **Health Check**
   - Path: `/health`
   - Interval: 30s

## Estructura de Archivos de Deploy

```
lead-ia/
├── Dockerfile                 # Imagen Docker principal
├── docker-compose.yml          # Desarrollo local
├── .dockerignore              # Archivos excluidos
├── Makefile                   # Comandos útiles
├── deploy/
│   ├── nginx.conf            # Configuración Nginx
│   ├── supervisor.conf      # Configuración Supervisor
│   ├── entrypoint.sh        # Script de inicialización
│   ├── start-backend.sh     # Inicio del backend
│   ├── init-db.sh           # Inicialización BD
│   ├── easypanel.json       # Config EasyPanel
│   └── CHECKLIST_DEPLOY.md  # Checklist de deploy
├── DEPLOY_EASYPANEL.md       # Guía completa de deploy
└── README_DEPLOY.md         # Este archivo
```

## Troubleshooting

### Error: No se puede conectar a PostgreSQL
```bash
# Verificar que PostgreSQL esté corriendo
docker-compose ps

# Ver logs de PostgreSQL
docker-compose logs postgres
```

### Error: Frontend no carga
```bash
# Verificar que el build se completó
docker-compose exec app ls -la /app/frontend/dist

# Ver logs de nginx
docker-compose exec app tail -f /var/log/supervisor/nginx.err.log
```

### Error: Backend no responde
```bash
# Ver logs del backend
docker-compose exec app tail -f /var/log/supervisor/backend.err.log

# Verificar estado de supervisor
docker-compose exec app supervisorctl status
```

## Credenciales por Defecto

**Superadmin:**
- Email: `devops@ideasdevops.com`
- Contraseña: `s3rv3rfa1l`

⚠️ **IMPORTANTE**: Cambiar estas credenciales en producción.

