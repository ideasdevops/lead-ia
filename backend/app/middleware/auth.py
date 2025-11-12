from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User

def require_permission(permission_name):
    """Decorador para requerir un permiso específico"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user or not user.is_active:
                return jsonify({'error': 'Usuario no autorizado'}), 403
            
            if not user.has_permission(permission_name):
                return jsonify({'error': 'Permisos insuficientes'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_role(role_name):
    """Decorador para requerir un rol específico"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user or not user.is_active:
                return jsonify({'error': 'Usuario no autorizado'}), 403
            
            if not user.has_role(role_name):
                return jsonify({'error': 'Rol insuficiente'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

