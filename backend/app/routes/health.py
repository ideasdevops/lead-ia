from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health():
    """Endpoint de health check para Docker/EasyPanel"""
    return jsonify({'status': 'healthy'}), 200

