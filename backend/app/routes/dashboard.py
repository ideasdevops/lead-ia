from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from datetime import datetime, timedelta
from app import db
from app.models import User, SearchQuery, Lead
from app.middleware.auth import require_permission

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
@require_permission('view_dashboard')
def get_stats():
    """Obtener estadísticas del dashboard"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Determinar si es superadmin
    is_superadmin = user.has_role('superadmin')
    
    # Construir queries base
    if is_superadmin:
        searches_query = SearchQuery.query
        leads_query = Lead.query
        users_query = User.query
    else:
        searches_query = SearchQuery.query.filter_by(user_id=user_id)
        leads_query = Lead.query.join(SearchQuery).filter(SearchQuery.user_id == user_id)
        users_query = User.query.filter_by(id=user_id)
    
    # Estadísticas generales
    total_searches = searches_query.count()
    total_leads = leads_query.count()
    total_users = users_query.count() if is_superadmin else 1
    
    # Búsquedas por estado
    searches_by_status = db.session.query(
        SearchQuery.status,
        func.count(SearchQuery.id)
    ).group_by(SearchQuery.status)
    
    if not is_superadmin:
        searches_by_status = searches_by_status.filter(SearchQuery.user_id == user_id)
    
    searches_by_status = dict(searches_by_status.all())
    
    # Leads por fuente
    leads_by_source = db.session.query(
        SearchQuery.source,
        func.count(Lead.id)
    ).join(Lead).group_by(SearchQuery.source)
    
    if not is_superadmin:
        leads_by_source = leads_by_source.filter(SearchQuery.user_id == user_id)
    
    leads_by_source = dict(leads_by_source.all())
    
    # Búsquedas recientes (últimas 7 días)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_searches = searches_query.filter(
        SearchQuery.created_at >= seven_days_ago
    ).count()
    
    # Leads recientes (últimos 7 días)
    recent_leads = leads_query.join(SearchQuery).filter(
        SearchQuery.created_at >= seven_days_ago
    ).count()
    
    # Búsquedas por mes (últimos 6 meses)
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    searches_by_month = db.session.query(
        func.date_trunc('month', SearchQuery.created_at).label('month'),
        func.count(SearchQuery.id).label('count')
    ).filter(SearchQuery.created_at >= six_months_ago)
    
    if not is_superadmin:
        searches_by_month = searches_by_month.filter(SearchQuery.user_id == user_id)
    
    searches_by_month = searches_by_month.group_by('month').order_by('month').all()
    
    return jsonify({
        'total_searches': total_searches,
        'total_leads': total_leads,
        'total_users': total_users,
        'searches_by_status': searches_by_status,
        'leads_by_source': leads_by_source,
        'recent_searches': recent_searches,
        'recent_leads': recent_leads,
        'searches_by_month': [
            {'month': row.month.isoformat(), 'count': row.count}
            for row in searches_by_month
        ]
    }), 200

