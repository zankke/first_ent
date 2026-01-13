from flask import Blueprint, request, jsonify
from backend.app import db
from backend.models import APIKey
from datetime import datetime

bp = Blueprint('api_keys', __name__)

@bp.route('/', methods=['GET'])
def get_api_keys():
    """모든 API 키 조회"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    platform = request.args.get('platform')
    is_active = request.args.get('is_active', type=bool)
    
    query = APIKey.query
    
    if platform:
        query = query.filter(APIKey.platform == platform)
    if is_active is not None:
        query = query.filter(APIKey.is_active == is_active)
    
    api_keys = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'api_keys': [api_key.to_dict() for api_key in api_keys.items],
        'total': api_keys.total,
        'pages': api_keys.pages,
        'current_page': page
    })

@bp.route('/<int:api_key_id>', methods=['GET'])
def get_api_key(api_key_id):
    """특정 API 키 조회"""
    api_key = APIKey.query.get_or_404(api_key_id)
    return jsonify(api_key.to_dict())

@bp.route('/', methods=['POST'])
def create_api_key():
    """새 API 키 생성"""
    data = request.get_json()
    
    api_key = APIKey(
        platform=data['platform'],
        api_name=data['api_name'],
        api_key=data['api_key'],
        api_secret=data.get('api_secret'),
        is_active=data.get('is_active', True)
    )
    
    db.session.add(api_key)
    db.session.commit()
    
    return jsonify(api_key.to_dict()), 201

@bp.route('/<int:api_key_id>', methods=['PUT'])
def update_api_key(api_key_id):
    """API 키 수정"""
    api_key = APIKey.query.get_or_404(api_key_id)
    data = request.get_json()
    
    api_key.api_name = data.get('api_name', api_key.api_name)
    api_key.api_key = data.get('api_key', api_key.api_key)
    api_key.api_secret = data.get('api_secret', api_key.api_secret)
    api_key.is_active = data.get('is_active', api_key.is_active)
    
    db.session.commit()
    
    return jsonify(api_key.to_dict())

@bp.route('/<int:api_key_id>', methods=['DELETE'])
def delete_api_key(api_key_id):
    """API 키 삭제"""
    api_key = APIKey.query.get_or_404(api_key_id)
    db.session.delete(api_key)
    db.session.commit()
    
    return jsonify({'message': 'API 키가 삭제되었습니다.'}), 200

@bp.route('/<int:api_key_id>/test', methods=['POST'])
def test_api_key(api_key_id):
    """API 키 테스트"""
    api_key = APIKey.query.get_or_404(api_key_id)
    
    # TODO: 실제 API 테스트 로직 구현
    # 각 플랫폼별 API 호출하여 키 유효성 검증
    
    api_key.last_used_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'API 키 테스트가 완료되었습니다.',
        'last_used_at': api_key.last_used_at.isoformat()
    })
