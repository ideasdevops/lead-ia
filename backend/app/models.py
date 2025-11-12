from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

# Tabla de asociación para roles y permisos
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)

# Tabla de asociación para usuarios y roles
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)  # Para signup controlado
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relaciones
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    search_queries = db.relationship('SearchQuery', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash y guarda la contraseña"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verifica la contraseña"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def has_permission(self, permission_name):
        """Verifica si el usuario tiene un permiso específico"""
        for role in self.roles:
            if role.has_permission(permission_name):
                return True
        return False
    
    def has_role(self, role_name):
        """Verifica si el usuario tiene un rol específico"""
        return any(role.name == role_name for role in self.roles)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'is_approved': self.is_approved,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'roles': [role.name for role in self.roles]
        }

class Role(db.Model):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relaciones
    permissions = db.relationship('Permission', secondary=role_permissions, 
                                  backref=db.backref('roles', lazy='dynamic'))
    
    def has_permission(self, permission_name):
        """Verifica si el rol tiene un permiso específico"""
        return any(perm.name == permission_name for perm in self.permissions)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'permissions': [perm.name for perm in self.permissions]
        }

class Permission(db.Model):
    __tablename__ = 'permission'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class SearchQuery(db.Model):
    __tablename__ = 'search_query'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    query = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(50), nullable=False)  # 'google_maps', 'yelp', etc.
    zoom = db.Column(db.Float, nullable=True)  # Para Google Maps
    status = db.Column(db.String(50), default='pending', nullable=False)  # pending, running, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relación
    leads = db.relationship('Lead', backref='search_query', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'query': self.query,
            'location': self.location,
            'source': self.source,
            'zoom': self.zoom,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'leads_count': len(self.leads)
        }

class Lead(db.Model):
    __tablename__ = 'lead'
    
    id = db.Column(db.Integer, primary_key=True)
    search_query_id = db.Column(db.Integer, db.ForeignKey('search_query.id'), nullable=False)
    title = db.Column(db.String(255), nullable=True)
    address = db.Column(db.Text, nullable=True)
    phone_number = db.Column(db.String(50), nullable=True)
    website_url = db.Column(db.String(500), nullable=True)
    tags = db.Column(db.String(500), nullable=True)  # Para Yelp
    source_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'search_query_id': self.search_query_id,
            'title': self.title,
            'address': self.address,
            'phone_number': self.phone_number,
            'website_url': self.website_url,
            'tags': self.tags,
            'source_url': self.source_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

