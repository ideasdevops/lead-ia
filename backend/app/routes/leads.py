from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Lead, SearchQuery
from app.middleware.auth import require_permission

leads_bp = Blueprint('leads', __name__)

@leads_bp.route('/list', methods=['GET'])
@jwt_required()
@require_permission('view_leads')
def list_leads():
    """Listar leads con filtros"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Parámetros de filtrado
    search_query_id = request.args.get('search_query_id', type=int)
    source = request.args.get('source')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    # Construir query
    query = Lead.query
    
    # Si no es superadmin, solo ver sus propios leads
    if not user.has_role('superadmin'):
        query = query.join(SearchQuery).filter(SearchQuery.user_id == user_id)
    
    if search_query_id:
        query = query.filter(Lead.search_query_id == search_query_id)
    
    if source:
        query = query.join(SearchQuery).filter(SearchQuery.source == source)
    
    # Paginación
    pagination = query.order_by(Lead.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'leads': [lead.to_dict() for lead in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@leads_bp.route('/<int:lead_id>', methods=['GET'])
@jwt_required()
@require_permission('view_leads')
def get_lead(lead_id):
    """Obtener un lead específico"""
    user_id = get_jwt_identity()
    lead = Lead.query.get_or_404(lead_id)
    user = User.query.get(user_id)
    
    # Verificar acceso
    if not user.has_role('superadmin') and lead.search_query.user_id != user_id:
        return jsonify({'error': 'No autorizado'}), 403
    
    return jsonify({'lead': lead.to_dict()}), 200

@leads_bp.route('/export', methods=['GET'])
@jwt_required()
@require_permission('export_leads')
def export_leads():
    """Exportar leads a CSV"""
    import csv
    import io
    from flask import Response
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Parámetros de filtrado
    search_query_id = request.args.get('search_query_id', type=int)
    source = request.args.get('source')
    
    # Construir query
    query = Lead.query
    
    if not user.has_role('superadmin'):
        query = query.join(SearchQuery).filter(SearchQuery.user_id == user_id)
    
    if search_query_id:
        query = query.filter(Lead.search_query_id == search_query_id)
    
    if source:
        query = query.join(SearchQuery).filter(SearchQuery.source == source)
    
    leads = query.all()
    
    # Crear CSV
    output = io.StringIO()
    fieldnames = ['id', 'title', 'address', 'phone_number', 'website_url', 'tags', 'source_url', 'created_at']
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for lead in leads:
        writer.writerow({
            'id': lead.id,
            'title': lead.title or '',
            'address': lead.address or '',
            'phone_number': lead.phone_number or '',
            'website_url': lead.website_url or '',
            'tags': lead.tags or '',
            'source_url': lead.source_url or '',
            'created_at': lead.created_at.isoformat() if lead.created_at else ''
        })
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=leads.csv'}
    )

