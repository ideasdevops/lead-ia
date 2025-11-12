# Lead-IA

Sistema completo de generación de leads con inteligencia artificial, frontend React y backend Flask.

## Descripción

Lead-IA es una plataforma completa para la generación y gestión de leads empresariales. El sistema permite realizar búsquedas automatizadas en Google Maps y Yelp, gestionar usuarios con roles y permisos, y visualizar resultados mediante un dashboard interactivo.

## Características Principales

- 🔍 **Búsqueda Automatizada**: Extracción de leads desde Google Maps y Yelp
- 📊 **Dashboard Interactivo**: Visualización de estadísticas y métricas
- 👥 **Gestión de Usuarios**: Sistema completo de roles y permisos
- 🔐 **Seguridad**: Autenticación JWT y control de acceso
- 📈 **Análisis de Datos**: Gráficos y reportes de búsquedas
- 📤 **Exportación**: Exportación de leads a CSV

## Estructura del Proyecto

```
Lead-IA/
├── backend/              # Backend Flask con PostgreSQL
├── frontend/             # Frontend React con TypeScript
└── py_lead_generation/    # Módulo de generación de leads
```

## Instalación Rápida

### Backend

```bash
cd backend
pip install -r requirements.txt
createdb lead_ia
python init_db.py
python run.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Credenciales de Acceso

**Superadmin:**
- Email: `devops@ideasdevops.com`
- Contraseña: `s3rv3rfa1l`

## Documentación

- [Guía de Instalación Completa](INSTALL.md)
- [Documentación del Frontend](README_FRONTEND.md)

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

## Repositorio

- **GitHub**: [ideasdevops/lead-ia](https://github.com/ideasdevops/lead-ia)
- **Email**: ideasdigitaldev@gmail.com

## Licencia

MIT
