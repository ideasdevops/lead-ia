# Guía de Despliegue - Lead-IA

## Preparación para GitHub

### 1. Inicializar Git (si no está inicializado)

```bash
cd /media/franco/RESPALDO-WIN2/DESARROLLOS_OWN_IDEASDEVOPS/lead-ia
git init
```

### 2. Configurar el repositorio remoto

```bash
git remote add origin git@github.com:ideasdevops/lead-ia.git
```

O si ya existe:
```bash
git remote set-url origin git@github.com:ideasdevops/lead-ia.git
```

### 3. Verificar configuración

```bash
git remote -v
```

Debería mostrar:
```
origin  git@github.com:ideasdevops/lead-ia.git (fetch)
origin  git@github.com:ideasdevops/lead-ia.git (push)
```

### 4. Agregar archivos

```bash
git add .
```

### 5. Commit inicial

```bash
git config user.name "ideasdevops"
git config user.email "ideasdigitaldev@gmail.com"
git commit -m "Initial commit: Lead-IA - Sistema completo de generación de leads"
```

### 6. Crear rama main (si es necesario)

```bash
git branch -M main
```

### 7. Subir al repositorio

```bash
git push -u origin main
```

## Estructura del Repositorio

El repositorio incluye:
- `/backend` - Código del backend Flask
- `/frontend` - Código del frontend React
- `/py_lead_generation` - Módulo de generación de leads
- `/archived` - Código archivado (versión anterior)
- Documentación (README.md, INSTALL.md, etc.)

## Archivos Excluidos (.gitignore)

Los siguientes archivos/directorios NO se subirán:
- `__pycache__/` y archivos `.pyc`
- `node_modules/`
- `.env` (variables de entorno)
- `venv/` o `env/` (entornos virtuales)
- `*.db`, `*.sqlite` (bases de datos locales)
- `.vscode/`, `.idea/` (configuraciones de IDE)

## Notas Importantes

1. **Nunca subir archivos .env** con credenciales reales
2. **Usar .env.example** como plantilla
3. **Verificar** que no haya información sensible en el código
4. **El superadmin** se crea automáticamente al inicializar la BD

## Configuración de GitHub

### Variables de Entorno (Secrets)

Para producción, configurar en GitHub Secrets:
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `DATABASE_URL`
- `CORS_ORIGINS`

### Protección de Ramas

Recomendado configurar:
- Protección de la rama `main`
- Requerir revisión de PRs
- Requerir que los tests pasen

## Siguientes Pasos

1. Verificar que el repositorio esté correctamente configurado
2. Revisar que todos los archivos necesarios estén incluidos
3. Verificar que los archivos sensibles estén en .gitignore
4. Hacer push al repositorio

