from app import create_app
import os
import sys

try:
    config_name = os.getenv('FLASK_ENV', 'production')
    print(f"📦 Creando aplicación Flask con configuración: {config_name}")
    
    app = create_app(config_name)
    
    print("✅ Aplicación Flask creada correctamente")
    
    if __name__ == '__main__':
        # IMPORTANTE: Flask debe usar puerto 5000, NO 80 (que es para Nginx)
        # Si PORT está configurado como 80, forzar 5000
        port_env = os.environ.get('PORT', '5000')
        try:
            port = int(port_env)
            # Si el puerto es 80, cambiarlo a 5000 (Nginx usa 80)
            if port == 80:
                print(f"⚠️  ADVERTENCIA: PORT=80 está reservado para Nginx, usando 5000")
                port = 5000
        except ValueError:
            print(f"⚠️  ADVERTENCIA: PORT inválido '{port_env}', usando 5000")
            port = 5000
        
        print(f"🌐 Iniciando servidor Flask en 0.0.0.0:{port}")
        app.run(debug=False, host='0.0.0.0', port=port, use_reloader=False)
except Exception as e:
    print(f"❌ ERROR CRÍTICO al crear/iniciar la aplicación: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
