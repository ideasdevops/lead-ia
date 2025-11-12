from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from app import db
from app.models import User, Role
from app.middleware.auth import require_permission, require_role

users_bp = Blueprint('users', __name__)

@users_bp.route('/list', methods=['GET'])
@jwt_required()
@require_permission('manage_users')
def list_users():
    """Listar todos los usuarios"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = User.query
    
    if search:
        query = query.filter(
            or_(
                User.email.ilike(f'%{search}%'),
                User.first_name.ilike(f'%{search}%'),
                User.last_name.ilike(f'%{search}%')
            )
        )
    
    pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'users': [user.to_dict() for user in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
@require_permission('manage_users')
def get_user(user_id):
    """Obtener un usuario específico"""
    user = User.query.get_or_404(user_id)
    return jsonify({'user': user.to_dict()}), 200

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@require_permission('manage_users')
def update_user(user_id):
    """Actualizar un usuario"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    # No permitir cambiar el email del superadmin
    if user.has_role('superadmin') and data.get('email') and data['email'] != user.email:
        return jsonify({'error': 'No se puede cambiar el email del superadmin'}), 400
    
    if 'email' in data:
        # Verificar que el email no esté en uso
        existing = User.query.filter_by(email=data['email']).first()
        if existing and existing.id != user_id:
            return jsonify({'error': 'El email ya está en uso'}), 400
        user.email = data['email']
    
    if 'first_name' in data:
        user.first_name = data['first_name']
    
    if 'last_name' in data:
        user.last_name = data['last_name']
    
    if 'is_active' in data:
        user.is_active = data['is_active']
    
    if 'is_approved' in data:
        user.is_approved = data['is_approved']
    
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    
    if 'roles' in data:
        # Actualizar roles
        role_names = data['roles']
        new_roles = Role.query.filter(Role.name.in_(role_names)).all()
        user.roles = new_roles
    
    db.session.commit()
    
    return jsonify({'user': user.to_dict()}), 200

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@require_role('superadmin')
def delete_user(user_id):
    """Eliminar un usuario"""
    user = User.query.get_or_404(user_id)
    
    # No permitir eliminar al superadmin
    if user.has_role('superadmin'):
        return jsonify({'error': 'No se puede eliminar al superadmin'}), 400
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'Usuario eliminado'}), 200

@users_bp.route('/<int:user_id>/approve', methods=['POST'])
@jwt_required()
@require_permission('approve_users')
def approve_user(user_id):
    """Aprobar un usuario pendiente"""
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    
    return jsonify({'message': 'Usuario aprobado', 'user': user.to_dict()}), 200

@users_bp.route('/pending', methods=['GET'])
@jwt_required()
@require_permission('approve_users')
def list_pending_users():
    """Listar usuarios pendientes de aprobación"""
    users = User.query.filter_by(is_approved=False).all()
    return jsonify({'users': [user.to_dict() for user in users]}), 200

