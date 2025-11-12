# 📦 Volúmenes Correctos para Lead-IA

## ⚠️ IMPORTANTE: Solo 2 Volúmenes Necesarios

Para Lead-IA, solo necesitas configurar **2 volúmenes**, no los 7 que aparecen en la imagen (esos son de otro proyecto).

## ✅ Volúmenes Requeridos

### Volumen 1: Logs
```
Tipo: VOLUME
Nombre: lead-ia-logs (o logs)
Ruta en Contenedor: /app/logs
Tamaño: 1GB
```

### Volumen 2: Database
```
Tipo: VOLUME
Nombre: lead-ia-database (o database)
Ruta en Contenedor: /app/database
Tamaño: 10GB
```

## ❌ Volúmenes que NO Necesitas

Los siguientes volúmenes que aparecen en la imagen son de OTRO proyecto y NO son necesarios para Lead-IA:

- ❌ `/data` - NO necesario
- ❌ `/data/cache` - NO necesario
- ❌ `/data/downloads` - NO necesario
- ❌ `/data/backups` - NO necesario
- ❌ `/etc/supervisor/conf.d` - NO necesario (la configuración está en la imagen)

## 📝 Configuración Correcta en EasyPanel

En la sección de "Mounts" de EasyPanel, debes tener solo:

1. **VOLUME** - Nombre: `logs` - Ruta: `/app/logs`
2. **VOLUME** - Nombre: `database` - Ruta: `/app/database`

Si tienes otros volúmenes, puedes eliminarlos o dejarlos (no harán daño, pero no se usarán).

## 🔍 Verificación

Después del deploy, puedes verificar que los volúmenes estén montados correctamente:

```bash
# Verificar que los directorios existen
ls -la /app/logs
ls -la /app/database
```

## 📚 Referencia

Para más detalles, ver:
- [VARIABLES_ENV.md](./VARIABLES_ENV.md)
- [EASYPANEL_CONFIG.md](./EASYPANEL_CONFIG.md)

