# Lead-IA - Frontend y Backend

Sistema completo de generación de leads con frontend React y backend Flask.

## Estructura del Proyecto

```
Lead-IA/
├── backend/          # Backend Flask con PostgreSQL
├── frontend/         # Frontend React con TypeScript
└── py_lead_generation/  # Módulo de generación de leads
```

## Instalación y Configuración

### Backend

1. Instalar dependencias:
```bash
cd backend
pip install -r requirements.txt
```

2. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales de PostgreSQL
```

3. Crear base de datos PostgreSQL:
```bash
createdb lead_ia
```

4. Inicializar base de datos:
```bash
python init_db.py
```

5. Ejecutar servidor:
```bash
python run.py
```

El backend estará disponible en `http://localhost:5000`

### Frontend

1. Instalar dependencias:
```bash
cd frontend
npm install
```

2. Ejecutar servidor de desarrollo:
```bash
npm run dev
```

El frontend estará disponible en `http://localhost:3000`

## Credenciales de Acceso

**Superadmin:**
- Email: `devops@ideasdevops.com`
- Contraseña: `s3rv3rfa1l`

## Características

### Dashboard Principal
- Estadísticas generales (búsquedas, leads, usuarios)
- Gráficos de búsquedas por estado y fuente
- Gráficos de búsquedas por mes

### Búsqueda y Prospección
- Crear nuevas búsquedas en Google Maps o Yelp
- Ejecutar búsquedas pendientes
- Ver historial de búsquedas

### Resultados
- Visualizar leads obtenidos
- Filtrar por búsqueda y fuente
- Exportar a CSV
- Paginación

### Gestión de Usuarios
- Listar usuarios
- Aprobar usuarios pendientes
- Editar usuarios
- Asignar roles
- Activar/desactivar usuarios

### Gestión de Roles y Permisos
- Crear y editar roles
- Asignar permisos a roles
- Gestionar permisos del sistema

## Permisos del Sistema

- `view_dashboard`: Ver dashboard
- `create_search`: Crear búsquedas
- `view_leads`: Ver leads
- `export_leads`: Exportar leads
- `manage_users`: Gestionar usuarios
- `manage_roles`: Gestionar roles
- `approve_users`: Aprobar usuarios

## Tecnologías

### Backend
- Flask
- SQLAlchemy
- PostgreSQL
- Flask-JWT-Extended
- Flask-CORS

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- React Query
- Recharts
- React Router
