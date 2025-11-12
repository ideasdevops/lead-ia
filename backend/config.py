import os
from datetime import timedelta

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Asegurar que DATABASE_URL use el esquema correcto para SQLAlchemy
    # SQLAlchemy requiere 'postgresql://' no 'postgres://'
    # IMPORTANTE: En producción, la base de datos está en un contenedor separado
    # Usar el nombre del servicio como hostname (ej: cloud_lead-ia-db)
    _db_url = os.environ.get('DATABASE_URL')
    if not _db_url:
        raise ValueError(
            "DATABASE_URL no está configurada. "
            "En producción, debe apuntar a un contenedor externo de PostgreSQL. "
            "Ejemplo: postgresql://usuario:contraseña@cloud_lead-ia-db:5432/leadia-db"
        )
    
    # Convertir postgres:// a postgresql:// si es necesario
    if isinstance(_db_url, str) and _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
        print(f"⚠️  Convertido postgres:// a postgresql:// en DATABASE_URL")
    
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

