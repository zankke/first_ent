"""
인증 관련 API 엔드포인트
현재 로그인한 사용자의 권한 정보 조회
"""
from flask import Blueprint, request, jsonify, g
from backend.utils.auth import require_auth, get_user_permission, verify_supabase_token
import logging

bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)


@bp.route('/me', methods=['GET'])
@require_auth
def get_current_user():
    """
    현재 로그인한 사용자의 정보 및 권한 조회
    """
    account = g.current_user
    
    return jsonify({
        'user': account.to_dict(),
        'email': g.user_email,
        'level': g.user_level,
        'permissions': {
            'can_create': g.user_level in ['admin', 'manager'],
            'can_edit': g.user_level in ['admin', 'manager'],
            'can_delete': g.user_level == 'admin',
            'can_view': True
        }
    })


@bp.route('/verify', methods=['POST'])
def verify_token():
    """
    토큰 검증 및 사용자 권한 정보 반환
    프론트엔드에서 사용
    """
    data = request.get_json()
    token = data.get('token') if data else None
    
    if not token:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
    
    if not token:
        return jsonify({'error': '토큰이 제공되지 않았습니다.'}), 400
    
    # 토큰 검증
    is_valid, user_email, error = verify_supabase_token(token)
    
    if not is_valid:
        return jsonify({
            'valid': False,
            'error': error or '토큰 검증 실패'
        }), 401
    
    # 권한 정보 조회
    permission = get_user_permission(user_email)
    
    if not permission['account']:
        return jsonify({
            'valid': True,
            'authenticated': False,
            'email': user_email,
            'message': '시스템에 등록되지 않은 사용자입니다.'
        }), 200
    
    response = jsonify({
        'valid': True,
        'authenticated': permission['has_permission'],
        'email': user_email,
        'account': permission['account'].to_dict(),
        'level': permission['level'],
        'status': permission['status'],
        'permissions': {
            'can_create': permission['level'] in ['admin', 'manager'],
            'can_edit': permission['level'] in ['admin', 'manager'],
            'can_delete': permission['level'] == 'admin',
            'can_view': True
        }
    })
    response.headers['X-User-Level'] = permission['level']
    return response

