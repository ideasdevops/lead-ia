from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from config import config
import os

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Configurar logging
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
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
    from werkzeug.exceptions import UnprocessableEntity
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"⚠️ Token expirado para ruta: {request.path if request else 'N/A'}")
        return jsonify({'error': 'Token expirado'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"❌ Token inválido: {error}")
        return jsonify({'error': 'Token inválido', 'details': str(error)}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"❌ Token no proporcionado: {error}")
        return jsonify({'error': 'Token no proporcionado', 'details': str(error)}), 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        import logging
        logger = logging.getLogger(__name__)
        logger.warning("⚠️ Token no es fresh")
        return jsonify({'error': 'Token no es fresh'}), 401
    
    # Manejar errores de validación (422) - puede venir de Flask-JWT-Extended o Flask
    @app.errorhandler(422)
    def handle_validation_error(e):
        """Manejar errores de validación de Flask-JWT-Extended o Flask"""
        import logging
        logger = logging.getLogger(__name__)
        error_details = str(e.description) if hasattr(e, 'description') else str(e)
        
        # Log detallado del error
        logger.error(f"❌ Error 422 (Validación): {error_details}")
        if request:
            logger.error(f"   Request path: {request.path}")
            logger.error(f"   Request method: {request.method}")
            auth_header = request.headers.get('Authorization', 'No Authorization header')
            logger.error(f"   Authorization header: {auth_header[:50] if len(auth_header) > 50 else auth_header}")
            logger.error(f"   All headers: {dict(request.headers)}")
        
        # Si el error parece ser de JWT, devolver un mensaje más específico
        if 'token' in error_details.lower() or 'jwt' in error_details.lower():
            return jsonify({
                'error': 'Error de autenticación JWT',
                'details': error_details,
                'path': request.path if request else None
            }), 401  # Cambiar a 401 si es un error de JWT
        
        return jsonify({
            'error': 'Error de validación',
            'details': error_details,
            'path': request.path if request else None
        }), 422
    
    # Manejar errores de BadRequest (400)
    @app.errorhandler(400)
    def handle_bad_request(e):
        """Manejar errores de solicitud incorrecta"""
        return jsonify({
            'error': 'Solicitud incorrecta',
            'details': str(e.description) if hasattr(e, 'description') else str(e)
        }), 400
    
    # Registrar blueprints
    from app.routes.health import health_bp
    from app.routes.auth import auth_bp
    from app.routes.leads import leads_bp
    from app.routes.search import search_bp
    from app.routes.users import users_bp
    from app.routes.roles import roles_bp
    from app.routes.dashboard import dashboard_bp
    
    # Registrar blueprints PRIMERO (tienen prioridad sobre la ruta catch-all)
    app.register_blueprint(health_bp)  # Sin prefijo para /health
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(leads_bp, url_prefix='/api/leads')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(roles_bp, url_prefix='/api/roles')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    
    # Servir archivos estáticos del frontend (AL FINAL, después de todos los blueprints)
    # El frontend está construido en /app/frontend/dist
    frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'frontend', 'dist')
    
    # Log para debugging
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"📁 Frontend dist path: {frontend_dist}")
    logger.info(f"📁 Frontend dist exists: {os.path.exists(frontend_dist)}")
    if os.path.exists(frontend_dist):
        logger.info(f"📁 Frontend dist contents: {os.listdir(frontend_dist)[:10]}")
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        """Servir el frontend construido - esta ruta catch-all debe estar al final"""
        # Los blueprints ya manejan /health y /api/*, así que esta ruta solo se ejecuta
        # para rutas que no coinciden con ningún blueprint
        
        logger.debug(f"🌐 Serviendo frontend - path: '{path}', frontend_dist: {frontend_dist}")
        
        # Si el path existe como archivo estático, servirlo
        if path and os.path.exists(os.path.join(frontend_dist, path)):
            logger.debug(f"✅ Sirviendo archivo estático: {path}")
            return send_from_directory(frontend_dist, path)
        
        # Si no, servir index.html (para SPA routing)
        index_path = os.path.join(frontend_dist, 'index.html')
        if os.path.exists(index_path):
            logger.debug(f"✅ Sirviendo index.html para SPA routing")
            return send_from_directory(frontend_dist, 'index.html')
        
        logger.warning(f"❌ Frontend not found - path: '{path}', frontend_dist exists: {os.path.exists(frontend_dist)}")
        return jsonify({'error': 'Frontend not found', 'path': path, 'frontend_dist': frontend_dist}), 404
    
    # NO crear tablas aquí - se crean en init_db.py
    # Esto evita errores y recreación innecesaria en cada reinicio
    # Las tablas se crean una sola vez durante la inicialización
    
    return app

