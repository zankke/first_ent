"""
인증 관련 API 엔드포인트
현재 로그인한 사용자의 권한 정보 조회
"""
from flask import Blueprint, request, jsonify, g, current_app
from backend.utils.auth import require_auth, get_user_permission, decode_auth_token, generate_auth_token # Updated import
from backend.models import Account
from ..app import db
import logging
import jwt
from datetime import datetime, timedelta

bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@bp.route('/login', methods=['POST'])
def login():
    """
    사용자 로그인 및 JWT 토큰 발급
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': '이메일과 비밀번호를 입력해주세요.'}), 400

    # Superadmin seeding/update logic
    if email == 'devops@sfai.im' and password == 'Sfaimyouv2025':
        account = Account.query.filter_by(uemail=email).first()
        if not account:
            account = Account(
                uid='devops',
                uname='Super Admin',
                uemail=email,
                level='admin',
                status='Y'
            )
            account.set_password(password)
            db.session.add(account)
            db.session.commit()
        else:
            # Force update level, status AND password to ensure access
            account.level = 'admin'
            account.status = 'Y'
            account.set_password(password)
            db.session.commit()

    account = Account.query.filter_by(uemail=email).first()

    if not account or not account.check_password(password):
        return jsonify({'error': '유효하지 않은 이메일 또는 비밀번호입니다.'}), 401

    # JWT 토큰 생성
    access_token = generate_auth_token(account.uemail, account.uqid, account.level)
    if not access_token:
        return jsonify({'error': '토큰 생성에 실패했습니다.'}), 500

    return jsonify({
        'access_token': access_token,
        'user': account.to_dict(),
        'level': account.level
    }), 200




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
    is_valid, user_email, error = decode_auth_token(token) # Updated to use decode_auth_token
    
    if not is_valid:
        return jsonify({
            'valid': False,
            'authenticated': False,
            'error': error or '토큰 검증 실패'
        }), 200 # Return 200 so frontend can handle it without Axios error
    
    # 권한 정보 조회
    permission = get_user_permission(user_email)
    
    if not permission['account']:
        return jsonify({
            'valid': True,
            'authenticated': False,
            'email': user_email,
            'message': '시스템에 등록되지 않은 사용자입니다.'
        }), 200
    
    final_authenticated = permission['has_permission']

    response = jsonify({
        'valid': True,
        'authenticated': final_authenticated,
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

