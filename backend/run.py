from app import create_app
import os
import sys

try:
    config_name = os.getenv('FLASK_ENV', 'production')
    print(f"📦 Creando aplicación Flask con configuración: {config_name}")
    
    app = create_app(config_name)
    
    print("✅ Aplicación Flask creada correctamente")
    
    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        print(f"🌐 Iniciando servidor en 0.0.0.0:{port}")
        app.run(debug=False, host='0.0.0.0', port=port)
except Exception as e:
    print(f"❌ ERROR CRÍTICO al crear/iniciar la aplicación: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
