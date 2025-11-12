from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import asyncio
import logging
from app import db
from app.models import User, SearchQuery, Lead
from app.middleware.auth import require_permission

search_bp = Blueprint('search', __name__)
logger = logging.getLogger(__name__)

@search_bp.route('/start', methods=['POST'])
@jwt_required()
@require_permission('create_search')
def start_search():
    """Iniciar una búsqueda de leads"""
    try:
        logger.info(f"🔍 Iniciando búsqueda - Headers: {dict(request.headers)}")
        data = request.get_json(force=True)  # force=True para manejar Content-Type incorrecto
        logger.info(f"📦 Datos recibidos: {data}")
    except Exception as e:
        logger.error(f"❌ Error al procesar JSON: {e}")
        return jsonify({'error': 'Error al procesar JSON', 'details': str(e)}), 400
    
    user_id = get_jwt_identity()
    logger.info(f"👤 Usuario ID: {user_id}")
    
    if not data or not data.get('query') or not data.get('location') or not data.get('source'):
        logger.warning(f"⚠️ Datos incompletos: {data}")
        return jsonify({
            'error': 'Query, location y source son requeridos',
            'received': data
        }), 400
    
    source = data['source']
    if source not in ['google_maps', 'yelp']:
        return jsonify({'error': 'Source debe ser google_maps o yelp'}), 400
    
    # Crear registro de búsqueda
    search_query = SearchQuery(
        user_id=user_id,
        query=data['query'],
        location=data['location'],
        source=source,
        zoom=data.get('zoom', 12) if source == 'google_maps' else None,
        status='pending'
    )
    
    db.session.add(search_query)
    db.session.commit()
    
    # Ejecutar búsqueda en background (aquí se integraría con py_lead_generation)
    # Por ahora retornamos el ID de la búsqueda
    # TODO: Implementar ejecución asíncrona real
    
    return jsonify({
        'message': 'Búsqueda iniciada',
        'search_query': search_query.to_dict()
    }), 201

@search_bp.route('/execute/<int:search_id>', methods=['POST'])
@jwt_required()
@require_permission('create_search')
def execute_search(search_id):
    """Ejecutar una búsqueda específica"""
    user_id = get_jwt_identity()
    search_query = SearchQuery.query.get_or_404(search_id)
    
    # Verificar que el usuario tenga acceso
    if search_query.user_id != user_id and not User.query.get(user_id).has_permission('manage_users'):
        return jsonify({'error': 'No autorizado'}), 403
    
    if search_query.status == 'running':
        return jsonify({'error': 'La búsqueda ya está en ejecución'}), 400
    
    # Marcar como en ejecución
    search_query.status = 'running'
    db.session.commit()
    
    try:
        # Importar y ejecutar el engine correspondiente
        import sys
        import os
        # Agregar el directorio raíz al path para importar py_lead_generation
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
        if root_dir not in sys.path:
            sys.path.insert(0, root_dir)
        
        if search_query.source == 'google_maps':
            from py_lead_generation import GoogleMapsEngine
            engine = GoogleMapsEngine(
                search_query.query,
                search_query.location,
                search_query.zoom or 12
            )
        elif search_query.source == 'yelp':
            from py_lead_generation import YelpEngine
            engine = YelpEngine(
                search_query.query,
                search_query.location
            )
        else:
            raise ValueError(f"Source no soportado: {search_query.source}")
        
        # Ejecutar búsqueda
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(engine.run())
        
        # Guardar resultados en la base de datos
        entries = engine.entries
        for entry in entries:
            lead = Lead(
                search_query_id=search_query.id,
                title=entry.get('Title', ''),
                address=entry.get('Address', ''),
                phone_number=entry.get('PhoneNumber', ''),
                website_url=entry.get('WebsiteURL', ''),
                tags=entry.get('Tags', '')
            )
            db.session.add(lead)
        
        search_query.status = 'completed'
        search_query.completed_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Búsqueda completada',
            'search_query': search_query.to_dict(),
            'leads_count': len(entries)
        }), 200
        
    except Exception as e:
        search_query.status = 'failed'
        db.session.commit()
        import traceback
        return jsonify({'error': f'Error en la búsqueda: {str(e)}', 'traceback': traceback.format_exc()}), 500

@search_bp.route('/list', methods=['GET'])
@jwt_required()
@require_permission('view_leads')
def list_searches():
    """Listar todas las búsquedas del usuario"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Si es superadmin, mostrar todas las búsquedas
    if user.has_role('superadmin'):
        searches = SearchQuery.query.order_by(SearchQuery.created_at.desc()).all()
    else:
        searches = SearchQuery.query.filter_by(user_id=user_id).order_by(SearchQuery.created_at.desc()).all()
    
    return jsonify({
        'searches': [s.to_dict() for s in searches]
    }), 200

@search_bp.route('/<int:search_id>', methods=['GET'])
@jwt_required()
@require_permission('view_leads')
def get_search(search_id):
    """Obtener detalles de una búsqueda"""
    user_id = get_jwt_identity()
    search_query = SearchQuery.query.get_or_404(search_id)
    user = User.query.get(user_id)
    
    # Verificar acceso
    if search_query.user_id != user_id and not user.has_role('superadmin'):
        return jsonify({'error': 'No autorizado'}), 403
    
    search_dict = search_query.to_dict()
    search_dict['leads'] = [lead.to_dict() for lead in search_query.leads]
    
    return jsonify({'search_query': search_dict}), 200

