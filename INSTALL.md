# Guía de Instalación - Lead-IA System

## Requisitos Previos

- Python 3.10 o superior
- Node.js 18 o superior
- PostgreSQL 12 o superior
- npm o yarn

## Instalación del Backend

1. **Navegar al directorio backend:**
```bash
cd backend
```

2. **Crear entorno virtual (recomendado):**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos PostgreSQL:**
```bash
# Crear base de datos
createdb lead_ia

# O usando psql:
psql -U postgres
CREATE DATABASE lead_ia;
\q
```

5. **Configurar variables de entorno:**
```bash
# Crear archivo .env en el directorio backend
SECRET_KEY=tu-secret-key-aqui
JWT_SECRET_KEY=tu-jwt-secret-key-aqui
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/lead_ia
FLASK_ENV=development
CORS_ORIGINS=http://localhost:3000
```

6. **Inicializar base de datos:**
```bash
python init_db.py
```

Esto creará:
- Todas las tablas necesarias
- El usuario superadmin (devops@ideasdevops.com / s3rv3rfa1l)
- Los permisos básicos del sistema

7. **Ejecutar el servidor:**
```bash
python run.py
```

El backend estará disponible en `http://localhost:5000`

## Instalación del Frontend

1. **Navegar al directorio frontend:**
```bash
cd frontend
```

2. **Instalar dependencias:**
```bash
npm install
```

3. **Ejecutar servidor de desarrollo:**
```bash
npm run dev
```

El frontend estará disponible en `http://localhost:3000`

## Instalación del Módulo py_lead_generation

El módulo `py_lead_generation` debe estar disponible. Si no está instalado:

```bash
# Desde el directorio raíz del proyecto
pip install -e .
```

O instalar desde PyPI:
```bash
pip install py-lead-generation
```

## Verificación de Instalación

1. **Backend:**
   - Abrir `http://localhost:5000/api/dashboard/stats` (requiere autenticación)
   - Debería retornar un error 401 si no estás autenticado (esto es correcto)

2. **Frontend:**
   - Abrir `http://localhost:3000`
   - Deberías ver la página de login

3. **Login inicial:**
   - Email: `devops@ideasdevops.com`
   - Contraseña: `s3rv3rfa1l`

## Solución de Problemas

### Error de conexión a PostgreSQL
- Verificar que PostgreSQL esté ejecutándose
- Verificar las credenciales en `.env`
- Verificar que la base de datos `lead_ia` exista

### Error al importar py_lead_generation
- Asegurarse de que el módulo esté instalado: `pip install -e .`
- Verificar que el path esté correcto en `search.py`

### Error CORS en el frontend
- Verificar que `CORS_ORIGINS` en `.env` incluya `http://localhost:3000`
- Verificar que el backend esté ejecutándose

### Error de migraciones
Si necesitas crear migraciones:
```bash
cd backend
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Estructura de la Base de Datos

El sistema crea las siguientes tablas:
- `user`: Usuarios del sistema
- `role`: Roles del sistema
- `permission`: Permisos disponibles
- `role_permissions`: Relación roles-permisos
- `user_roles`: Relación usuarios-roles
- `search_query`: Búsquedas realizadas
- `lead`: Leads obtenidos

## Próximos Pasos

1. Iniciar sesión con el superadmin
2. Crear nuevos usuarios desde el panel de administración
3. Asignar roles y permisos
4. Realizar tu primera búsqueda de leads
