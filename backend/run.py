from app import create_app
import os
import sys

# EasyPanel maneja Nginx automáticamente
# Flask debe escuchar en el puerto que EasyPanel configure (por defecto 80)
# Si PORT no está configurado, usar 80
if 'PORT' not in os.environ:
    os.environ['PORT'] = '80'

try:
    config_name = os.getenv('FLASK_ENV', 'production')
    print(f"📦 Creando aplicación Flask con configuración: {config_name}")
    
    app = create_app(config_name)
    
    print("✅ Aplicación Flask creada correctamente")
    
    if __name__ == '__main__':
        # EasyPanel maneja Nginx automáticamente
        # Flask escucha en el puerto configurado por EasyPanel (típicamente 80)
        port = int(os.environ.get('PORT', 80))
        
        print(f"🌐 Iniciando servidor Flask en 0.0.0.0:{port}")
        print(f"📋 EasyPanel maneja el reverse proxy automáticamente")
        
        # Iniciar Flask en el puerto configurado
        app.run(debug=False, host='0.0.0.0', port=port, use_reloader=False)
except Exception as e:
    print(f"❌ ERROR CRÍTICO al crear/iniciar la aplicación: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
