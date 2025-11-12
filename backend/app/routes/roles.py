from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Role, Permission
from app.middleware.auth import require_permission

roles_bp = Blueprint('roles', __name__)

@roles_bp.route('/list', methods=['GET'])
@jwt_required()
@require_permission('manage_roles')
def list_roles():
    """Listar todos los roles"""
    roles = Role.query.all()
    return jsonify({'roles': [role.to_dict() for role in roles]}), 200

@roles_bp.route('/<int:role_id>', methods=['GET'])
@jwt_required()
@require_permission('manage_roles')
def get_role(role_id):
    """Obtener un rol específico"""
    role = Role.query.get_or_404(role_id)
    return jsonify({'role': role.to_dict()}), 200

@roles_bp.route('/create', methods=['POST'])
@jwt_required()
@require_permission('manage_roles')
def create_role():
    """Crear un nuevo rol"""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'El nombre del rol es requerido'}), 400
    
    # Verificar que el rol no exista
    if Role.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'El rol ya existe'}), 400
    
    role = Role(
        name=data['name'],
        description=data.get('description', '')
    )
    
    # Asignar permisos si se proporcionan
    if 'permissions' in data:
        permission_names = data['permissions']
        permissions = Permission.query.filter(Permission.name.in_(permission_names)).all()
        role.permissions = permissions
    
    db.session.add(role)
    db.session.commit()
    
    return jsonify({'role': role.to_dict()}), 201

@roles_bp.route('/<int:role_id>', methods=['PUT'])
@jwt_required()
@require_permission('manage_roles')
def update_role(role_id):
    """Actualizar un rol"""
    role = Role.query.get_or_404(role_id)
    data = request.get_json()
    
    # No permitir cambiar el nombre del superadmin
    if role.name == 'superadmin' and data.get('name') and data['name'] != 'superadmin':
        return jsonify({'error': 'No se puede cambiar el nombre del rol superadmin'}), 400
    
    if 'name' in data and data['name'] != role.name:
        # Verificar que el nuevo nombre no esté en uso
        existing = Role.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': 'El nombre del rol ya está en uso'}), 400
        role.name = data['name']
    
    if 'description' in data:
        role.description = data['description']
    
    if 'permissions' in data:
        permission_names = data['permissions']
        permissions = Permission.query.filter(Permission.name.in_(permission_names)).all()
        role.permissions = permissions
    
    db.session.commit()
    
    return jsonify({'role': role.to_dict()}), 200

@roles_bp.route('/<int:role_id>', methods=['DELETE'])
@jwt_required()
@require_permission('manage_roles')
def delete_role(role_id):
    """Eliminar un rol"""
    role = Role.query.get_or_404(role_id)
    
    # No permitir eliminar el rol superadmin
    if role.name == 'superadmin':
        return jsonify({'error': 'No se puede eliminar el rol superadmin'}), 400
    
    db.session.delete(role)
    db.session.commit()
    
    return jsonify({'message': 'Rol eliminado'}), 200

@roles_bp.route('/permissions', methods=['GET'])
@jwt_required()
@require_permission('manage_roles')
def list_permissions():
    """Listar todos los permisos disponibles"""
    permissions = Permission.query.all()
    return jsonify({'permissions': [perm.to_dict() for perm in permissions]}), 200

