"""
Script para inicializar la base de datos PostgreSQL
Ejecutar: python init_db.py
"""
import os
from app import create_app, db
from app.models import User, Role, Permission
from app.utils.auth import create_superadmin

def init_database():
    """Inicializa la base de datos y crea el superadmin"""
    app = create_app()
    
    with app.app_context():
        # Crear todas las tablas
        print("Creando tablas...")
        db.create_all()
        print("✓ Tablas creadas")
        
        # Crear superadmin
        print("Creando superadmin...")
        create_superadmin()
        print("✓ Superadmin creado")
        
        print("\n✓ Base de datos inicializada correctamente")
        print(f"  Superadmin: devops@ideasdevops.com")
        print(f"  Contraseña: s3rv3rfa1l")

if __name__ == '__main__':
    init_database()

