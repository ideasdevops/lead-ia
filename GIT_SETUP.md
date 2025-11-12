# Configuración de Git para Lead-IA

## Comandos para subir al repositorio

### 1. Verificar estado actual

```bash
cd /media/franco/RESPALDO-WIN2/DESARROLLOS_OWN_IDEASDEVOPS/lead-ia
git status
```

### 2. Configurar usuario de Git (si no está configurado)

```bash
git config user.name "ideasdevops"
git config user.email "ideasdigitaldev@gmail.com"
```

### 3. Inicializar repositorio (si no está inicializado)

```bash
git init
```

### 4. Agregar repositorio remoto

```bash
git remote add origin git@github.com:ideasdevops/lead-ia.git
```

O si ya existe, actualizar:
```bash
git remote set-url origin git@github.com:ideasdevops/lead-ia.git
```

### 5. Verificar remoto

```bash
git remote -v
```

Debería mostrar:
```
origin  git@github.com:ideasdevops/lead-ia.git (fetch)
origin  git@github.com:ideasdevops/lead-ia.git (push)
```

### 6. Agregar todos los archivos

```bash
git add .
```

### 7. Hacer commit inicial

```bash
git commit -m "Initial commit: Lead-IA - Sistema completo de generación de leads con frontend y backend"
```

### 8. Crear y cambiar a rama main

```bash
git branch -M main
```

### 9. Subir al repositorio

```bash
git push -u origin main
```

## Si el repositorio ya existe en GitHub

Si el repositorio ya tiene contenido, primero hacer pull:

```bash
git pull origin main --allow-unrelated-histories
```

Luego resolver conflictos si los hay y hacer push:

```bash
git push -u origin main
```

## Verificación

Después de subir, verificar en GitHub:
- https://github.com/ideasdevops/lead-ia

## Notas Importantes

1. **Nunca subir archivos .env** con credenciales reales
2. Verificar que `.gitignore` esté configurado correctamente
3. El archivo `.env.example` se subirá como plantilla
4. Los archivos en `archived/` se mantendrán para referencia histórica

