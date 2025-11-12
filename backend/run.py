from app import create_app
import os
import sys

# CRÍTICO: Forzar PORT=3005 ANTES de importar cualquier cosa
# Esto asegura que Flask siempre use el puerto correcto
os.environ['PORT'] = '3005'

try:
    config_name = os.getenv('FLASK_ENV', 'production')
    print(f"📦 Creando aplicación Flask con configuración: {config_name}")
    
    app = create_app(config_name)
    
    print("✅ Aplicación Flask creada correctamente")
    
    if __name__ == '__main__':
        # SIEMPRE usar puerto 3005 - hardcoded, sin excepciones
        # Nginx usa puerto 80, Flask usa puerto 3005
        port = 3005
        
        print(f"🌐 Iniciando servidor Flask en 0.0.0.0:{port}")
        print(f"📋 PORT forzado a 3005 (Nginx usa 80)")
        
        # Iniciar Flask con puerto 3005 explícitamente
        app.run(debug=False, host='0.0.0.0', port=3005, use_reloader=False)
except Exception as e:
    print(f"❌ ERROR CRÍTICO al crear/iniciar la aplicación: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
