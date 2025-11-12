from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Verificar y corregir DATABASE_URL si es necesario (por si acaso)
    db_url = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if db_url and isinstance(db_url, str) and db_url.startswith('postgres://'):
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace('postgres://', 'postgresql://', 1)
        print(f"⚠️  Corregido DATABASE_URL en create_app: postgres:// -> postgresql://")
    
    # Debug: mostrar URL de base de datos (sin contraseña)
    if db_url:
        safe_url = db_url.split('@')[-1] if '@' in db_url else db_url
        print(f"📦 Usando base de datos: ...@{safe_url}")
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    # Registrar blueprints
    from app.routes.health import health_bp
    from app.routes.auth import auth_bp
    from app.routes.leads import leads_bp
    from app.routes.search import search_bp
    from app.routes.users import users_bp
    from app.routes.roles import roles_bp
    from app.routes.dashboard import dashboard_bp
    
    app.register_blueprint(health_bp)  # Sin prefijo para /health
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(leads_bp, url_prefix='/api/leads')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(roles_bp, url_prefix='/api/roles')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    
    # Crear tablas en la primera ejecución
    with app.app_context():
        db.create_all()
        # Crear superadmin si no existe
        from app.models import User, Role
        from app.utils.auth import create_superadmin
        create_superadmin()
    
    return app

