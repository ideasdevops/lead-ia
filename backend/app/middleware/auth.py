from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.exceptions import JWTDecodeError, NoAuthorizationError
from app.models import User

def require_permission(permission_name):
    """Decorador para requerir un permiso específico"""
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
                
                if not user.has_permission(permission_name):
                    return jsonify({'error': 'Permisos insuficientes'}), 403
                
                return f(*args, **kwargs)
            except (JWTDecodeError, NoAuthorizationError) as e:
                return jsonify({'error': 'Token inválido o no proporcionado', 'details': str(e)}), 401
            except Exception as e:
                return jsonify({'error': 'Error de autenticación', 'details': str(e)}), 500
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

