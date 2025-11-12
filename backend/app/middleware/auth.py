from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.exceptions import JWTDecodeError, NoAuthorizationError
import logging
from app.models import User

logger = logging.getLogger(__name__)

def require_permission(permission_name):
    """Decorador para requerir un permiso específico"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                logger.info(f"🔐 Verificando permiso '{permission_name}' para ruta {request.path}")
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                logger.info(f"👤 Usuario ID obtenido del token: {user_id}")
                
                if not user_id:
                    logger.warning("⚠️ Token inválido o expirado - user_id es None")
                    return jsonify({'error': 'Token inválido o expirado'}), 401
                
                user = User.query.get(user_id)
                
                if not user:
                    logger.error(f"❌ Usuario no encontrado con ID: {user_id}")
                    return jsonify({'error': 'Usuario no encontrado'}), 404
                
                if not user.is_active:
                    logger.warning(f"⚠️ Usuario inactivo: {user.email}")
                    return jsonify({'error': 'Usuario inactivo'}), 403
                
                user_permissions = [perm.name for role in user.roles for perm in role.permissions]
                logger.info(f"📋 Permisos del usuario {user.email}: {user_permissions}")
                
                if not user.has_permission(permission_name):
                    logger.warning(f"⚠️ Usuario {user.email} no tiene permiso '{permission_name}'")
                    return jsonify({
                        'error': 'Permisos insuficientes',
                        'required_permission': permission_name,
                        'user_permissions': user_permissions
                    }), 403
                
                logger.info(f"✅ Permiso '{permission_name}' verificado correctamente")
                return f(*args, **kwargs)
            except (JWTDecodeError, NoAuthorizationError) as e:
                logger.error(f"❌ Error JWT: {e}")
                return jsonify({'error': 'Token inválido o no proporcionado', 'details': str(e)}), 401
            except Exception as e:
                import traceback
                logger.error(f"❌ Error inesperado en autenticación: {e}\n{traceback.format_exc()}")
                return jsonify({
                    'error': 'Error de autenticación',
                    'details': str(e),
                    'traceback': traceback.format_exc()
                }), 500
        return decorated_function
    return decorator

def require_role(role_name):
    """Decorador para requerir un rol específico"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                
                if not user_id:
                    return jsonify({'error': 'Token inválido o expirado'}), 401
                
                user = User.query.get(user_id)
                
                if not user:
                    return jsonify({'error': 'Usuario no encontrado'}), 404
                
                if not user.is_active:
                    return jsonify({'error': 'Usuario inactivo'}), 403
                
                if not user.has_role(role_name):
                    return jsonify({'error': 'Rol insuficiente'}), 403
                
                return f(*args, **kwargs)
            except (JWTDecodeError, NoAuthorizationError) as e:
                return jsonify({'error': 'Token inválido o no proporcionado', 'details': str(e)}), 401
            except Exception as e:
                return jsonify({'error': 'Error de autenticación', 'details': str(e)}), 500
        return decorated_function
    return decorator

