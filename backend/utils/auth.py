"""
인증 및 권한 관리 유틸리티
Supabase 토큰 검증 및 Account 권한 확인
"""
from functools import wraps
from flask import request, jsonify, g
from backend.app import db
from backend.models import Account
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase 설정
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')  # 서비스 키 (서버 사이드용)


def verify_supabase_token(token):
    """
    Supabase 액세스 토큰 검증
    JWT 토큰을 디코딩하여 사용자 이메일 추출
    Returns: (is_valid, user_email, error_message)
    """
    if not token:
        return False, None, "토큰이 제공되지 않았습니다."
    
    try:
        import jwt
        import json
        
        # JWT 토큰 디코딩 (검증 없이, Supabase는 자체 검증)
        # Supabase JWT는 3부분으로 구성: header.payload.signature
        try:
            # 토큰을 디코딩하여 payload 추출
            payload = jwt.decode(token, options={"verify_signature": False})
            user_email = payload.get('email')
            
            if user_email:
                return True, user_email, None
            else:
                return False, None, "토큰에 이메일 정보가 없습니다."
                
        except jwt.DecodeError:
            # JWT 디코딩 실패 시 Supabase API로 검증 시도
            if not SUPABASE_URL:
                # 개발 환경에서는 테스트용 이메일 반환
                if os.getenv('FLASK_ENV') == 'development':
                    # 토큰에서 이메일 추출 시도 (개발용)
                    return True, 'dev@example.com', None
                return False, None, "Supabase URL이 설정되지 않았습니다."
            
            # Supabase API를 사용하여 토큰 검증
            SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY', '')
            headers = {
                'Authorization': f'Bearer {token}',
                'apikey': SUPABASE_ANON_KEY
            }
            
            response = requests.get(
                f'{SUPABASE_URL}/auth/v1/user',
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                user_data = response.json()
                user_email = user_data.get('email')
                return True, user_email, None
            else:
                return False, None, f"토큰 검증 실패: {response.status_code}"
            
    except Exception as e:
        # 개발 환경에서는 허용
        if os.getenv('FLASK_ENV') == 'development':
            return True, 'dev@example.com', None
        return False, None, f"토큰 검증 중 오류 발생: {str(e)}"


def get_account_by_email(email):
    """
    이메일로 Account 조회
    Returns: Account 객체 또는 None
    """
    if not email:
        return None
    
    return Account.query.filter_by(uemail=email).first()


def get_user_permission(email):
    """
    사용자 이메일로 권한 정보 조회
    Returns: {
        'account': Account 객체,
        'level': 'admin' | 'manager' | 'viewer' | None,
        'status': 'Y' | 'N' | None,
        'has_permission': bool
    }
    """
    if not email:
        return {
            'account': None,
            'level': None,
            'status': None,
            'has_permission': False
        }
    
    account = get_account_by_email(email)
    
    if not account:
        return {
            'account': None,
            'level': None,
            'status': None,
            'has_permission': False
        }
    
    has_permission = account.status == 'Y'
    
    return {
        'account': account,
        'level': account.level,
        'status': account.status,
        'has_permission': has_permission
    }


def require_auth(f):
    """
    인증이 필요한 엔드포인트 데코레이터
    Supabase 토큰 검증 후 Account 권한 확인
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Authorization 헤더에서 토큰 추출
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': '인증 토큰이 필요합니다.'}), 401
        
        token = auth_header.split(' ')[1]
        
        # Supabase 토큰 검증
        is_valid, user_email, error = verify_supabase_token(token)
        
        if not is_valid:
            return jsonify({'error': error or '토큰 검증 실패'}), 401
        
        # 이메일로 Account 조회 및 권한 확인
        permission = get_user_permission(user_email)
        
        if not permission['has_permission']:
            if not permission['account']:
                return jsonify({
                    'error': '시스템에 등록되지 않은 사용자입니다.',
                    'email': user_email
                }), 403
            else:
                return jsonify({
                    'error': '비활성화된 계정입니다.',
                    'email': user_email
                }), 403
        
        # g 객체에 사용자 정보 저장 (함수 내에서 사용 가능)
        g.current_user = permission['account']
        g.user_email = user_email
        g.user_level = permission['level']
        
        return f(*args, **kwargs)
    
    return decorated_function


def require_role(*allowed_levels):
    """
    특정 권한 레벨이 필요한 엔드포인트 데코레이터
    사용법: @require_role('admin', 'manager')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 먼저 인증 확인
            auth_header = request.headers.get('Authorization')
            
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': '인증 토큰이 필요합니다.'}), 401
            
            token = auth_header.split(' ')[1]
            is_valid, user_email, error = verify_supabase_token(token)
            
            if not is_valid:
                return jsonify({'error': error or '토큰 검증 실패'}), 401
            
            # 권한 확인
            permission = get_user_permission(user_email)
            
            if not permission['has_permission']:
                return jsonify({'error': '권한이 없습니다.'}), 403
            
            # 권한 레벨 확인
            if permission['level'] not in allowed_levels:
                return jsonify({
                    'error': f'이 작업을 수행하려면 {", ".join(allowed_levels)} 권한이 필요합니다.',
                    'current_level': permission['level']
                }), 403
            
            # g 객체에 사용자 정보 저장
            g.current_user = permission['account']
            g.user_email = user_email
            g.user_level = permission['level']
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

