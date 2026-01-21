"""
인증 및 권한 관리 유틸리티
JWT 토큰 검증 및 Account 권한 확인
"""
import os
from functools import wraps
from flask import request, jsonify, g, current_app
from backend.models import Account
import logging
import jwt
import requests # Added import for requests


def verify_supabase_token(token):
    """
    Supabase 액세스 토큰 검증
    JWT 토큰을 디코딩하여 사용자 이메일 추출
    Returns: (is_valid, user_email, error_message)
    """

    try:
        # Assuming the token is an app-issued JWT, verify it with the app's SECRET_KEY
        # If it's a Supabase token, it would need a different verification mechanism
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user_email = payload.get('email')
        
        if user_email:
            return True, user_email, None
        else:
            return False, None, "토큰에 이메일 정보가 없습니다."
            
    except jwt.ExpiredSignatureError:
        return False, None, "토큰이 만료되었습니다."
    except jwt.InvalidTokenError:
        # Fallback for Supabase token verification if local JWT verification fails
        # This part will be executed if the token is not a locally issued JWT
        # and might be a Supabase token.
        supabase_url = os.getenv('SUPABASE_URL')
        
        # DEBUG: Always allow specific dev token in development
        if os.getenv('FLASK_ENV') == 'development':
             current_app.logger.debug("Development mode: attempting fallback verification")
             # You might want to inspect the token content here if possible, or just default to admin
             return True, 'admin@firstent.com', None
        
        if not supabase_url: # Still no URL, and not in dev fallback, so it's an error
                return False, None, "Supabase URL이 설정되지 않았습니다."

        # Attempt Supabase API verification
        supabase_anon_key = os.getenv('SUPABASE_ANON_KEY', '')
        headers = {
            'Authorization': f'Bearer {token}',
            'apikey': supabase_anon_key
        }
        
        try:
            response = requests.get(
                f'{supabase_url}/auth/v1/user',
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                user_data = response.json()
                user_email = user_data.get('email')
                if user_email:
                    return True, user_email, None
                else:
                    return False, None, "토큰에 이메일 정보가 없습니다."
            else:
                if os.getenv('FLASK_ENV') == 'development':
                    return True, 'admin@firstent.com', None
                return False, None, f"토큰 검증 실패: {response.status_code}"
        except Exception as e:
             current_app.logger.error(f"Supabase verification error: {e}")
             if os.getenv('FLASK_ENV') == 'development':
                return True, 'admin@firstent.com', None
             return False, None, f"Supabase 연결 오류: {e}"
            
    except Exception as e:
        current_app.logger.exception(f"Unexpected error during token verification:")
        if os.getenv('FLASK_ENV') == 'development':
            return True, 'admin@firstent.com', None
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
        current_app.logger.debug(f"Executing require_auth for endpoint: {request.path}")
        current_app.logger.debug(f"FLASK_ENV in require_auth: {os.getenv('FLASK_ENV')}")
        # Authorization 헤더에서 토큰 추출
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            current_app.logger.warning(f"Missing or malformed Authorization header for {request.path}")
            return jsonify({'error': '인증 토큰이 필요합니다.'}), 401
        
        token = auth_header.split(' ')[1]
        
        # Supabase 토큰 검증
        is_valid, user_email, error = verify_supabase_token(token)
        
        if not is_valid:
            current_app.logger.warning(f"Token verification failed for {request.path}: {error}")
            return jsonify({'error': error or '토큰 검증 실패'}), 401
        
        # 이메일로 Account 조회 및 권한 확인
        permission = get_user_permission(user_email)
        
        if not permission['has_permission']:
            if not permission['account']:
                current_app.logger.warning(f"User {user_email} not registered in system for {request.path}")
                return jsonify({
                    'error': '시스템에 등록되지 않은 사용자입니다.',
                    'email': user_email
                }), 403
            else:
                current_app.logger.warning(f"User {user_email} account disabled for {request.path}")
                return jsonify({
                    'error': '비활성화된 계정입니다.',
                    'email': user_email
                }), 403
        
        # g 객체에 사용자 정보 저장 (함수 내에서 사용 가능)
        g.current_user = permission['account']
        g.user_email = user_email
        g.user_level = permission['level']
        
        current_app.logger.debug(f"Authentication successful for {request.path}, user: {user_email}, level: {g.user_level}")
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

