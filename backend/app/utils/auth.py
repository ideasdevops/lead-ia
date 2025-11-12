from app import db
from app.models import User, Role, Permission

def create_superadmin():
    """Crea el usuario superadmin si no existe"""
    superadmin_email = 'devops@ideasdevops.com'
    superadmin_password = 's3rv3rfa1l'
    
    # Verificar si ya existe
    if User.query.filter_by(email=superadmin_email).first():
        return
    
    # Crear permisos básicos si no existen
    permissions = {
        'view_dashboard': Permission(name='view_dashboard', description='Ver dashboard'),
        'create_search': Permission(name='create_search', description='Crear búsquedas'),
        'view_leads': Permission(name='view_leads', description='Ver leads'),
        'export_leads': Permission(name='export_leads', description='Exportar leads'),
        'manage_users': Permission(name='manage_users', description='Gestionar usuarios'),
        'manage_roles': Permission(name='manage_roles', description='Gestionar roles'),
        'approve_users': Permission(name='approve_users', description='Aprobar usuarios'),
    }
    
    for perm in permissions.values():
        if not Permission.query.filter_by(name=perm.name).first():
            db.session.add(perm)
    
    db.session.commit()
    
    # Crear rol superadmin
    superadmin_role = Role.query.filter_by(name='superadmin').first()
    if not superadmin_role:
        superadmin_role = Role(name='superadmin', description='Administrador con todos los permisos')
        db.session.add(superadmin_role)
        db.session.commit()
        
        # Asignar todos los permisos al rol superadmin
        for perm in Permission.query.all():
            superadmin_role.permissions.append(perm)
        db.session.commit()
    
    # Crear usuario superadmin
    superadmin = User(
        email=superadmin_email,
        first_name='Super',
        last_name='Admin',
        is_active=True,
        is_approved=True
    )
    superadmin.set_password(superadmin_password)
    superadmin.roles.append(superadmin_role)
    
    db.session.add(superadmin)
    db.session.commit()
    
    print(f"Superadmin creado: {superadmin_email}")

