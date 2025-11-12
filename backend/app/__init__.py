from flask import Flask, jsonify
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
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # CRÍTICO: Convertir postgres:// a postgresql:// ANTES de inicializar SQLAlchemy
    # SQLAlchemy requiere postgresql:// y falla con postgres://
    db_url = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if db_url and isinstance(db_url, str):
        original_url = db_url
        # Convertir postgres:// a postgresql://
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
            app.config['SQLALCHEMY_DATABASE_URI'] = db_url
            print(f"⚠️  CONVERTIDO postgres:// -> postgresql:// en create_app")
            print(f"   Original: {original_url[:30]}...")
            print(f"   Nuevo:    {db_url[:30]}...")
        
        # Debug: mostrar URL de base de datos (sin contraseña)
        safe_url = db_url.split('@')[-1] if '@' in db_url else db_url
        print(f"📦 Usando base de datos: ...@{safe_url}")
    
    # Inicializar extensiones (ahora con la URL correcta)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    # Configurar manejo de errores de JWT
    from flask_jwt_extended.exceptions import JWTDecodeError, NoAuthorizationError
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token expirado'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Token inválido', 'details': str(error)}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Token no proporcionado', 'details': str(error)}), 401
    
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
    
    # NO crear tablas aquí - se crean en init_db.py
    # Esto evita errores y recreación innecesaria en cada reinicio
    # Las tablas se crean una sola vez durante la inicialización
    
    return app

