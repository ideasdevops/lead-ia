from app import create_app
import os
import sys

try:
    config_name = os.getenv('FLASK_ENV', 'production')
    print(f"📦 Creando aplicación Flask con configuración: {config_name}")
    
    app = create_app(config_name)
    
    print("✅ Aplicación Flask creada correctamente")
    
    if __name__ == '__main__':
        # CRÍTICO: Flask DEBE usar puerto 5000, NO 80 (que es para Nginx)
        # Forzar puerto 5000 sin importar qué diga la variable de entorno
        port_env = os.environ.get('PORT', '5000')
        print(f"📦 PORT de entorno: {port_env}")
        
        # SIEMPRE usar puerto 5000, ignorar cualquier otra configuración
        port = 5000
        if port_env and str(port_env) != '5000':
            print(f"⚠️  ADVERTENCIA: PORT={port_env} ignorado, usando 5000 (Nginx usa 80)")
            # Eliminar PORT del entorno para evitar confusiones
            if 'PORT' in os.environ:
                del os.environ['PORT']
        
        print(f"🌐 Iniciando servidor Flask en 0.0.0.0:{port}")
        print(f"📋 Variables de entorno PORT: {os.environ.get('PORT', 'NO CONFIGURADA')}")
        app.run(debug=False, host='0.0.0.0', port=port, use_reloader=False)
except Exception as e:
    print(f"❌ ERROR CRÍTICO al crear/iniciar la aplicación: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
