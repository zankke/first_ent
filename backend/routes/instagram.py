from flask import Blueprint, request, jsonify, abort
import logging
from datetime import datetime
from urllib.parse import quote_plus
import requests
import os

from ..app import db
from backend.models import InstagramUser, InstagramSearchResult, InstagramProfilePic, InstagramBioLink, InstagramBusinessContact
from backend.config.instagram_config import InstagramAPIConfig
from backend.services.instagram_service import InstagramService

logger = logging.getLogger(__name__)

bp = Blueprint('instagram', __name__, url_prefix='/api/instagram')

class InstagramAPIClient:
    """RapidAPI를 통한 Instagram API 클라이언트"""
    
    def __init__(self, config: InstagramAPIConfig):
        self.config = config
        self.base_url = config.BASE_URL
        self.headers = {
            'x-rapidapi-host': config.RAPIDAPI_HOST,
            'x-rapidapi-key': config.RAPIDAPI_KEY,
            'Content-Type': 'application/json'
        }
    
    def search_instagram_user(self, username: str) -> dict or None:
        """Instagram 사용자 검색"""
        try:
            url = f"{self.base_url}/api/ig/search"
            params = {
                'ig_handle': username,
                'language': 'en'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Instagram API 요청 실패: {str(e)}")
            return None
    
    def get_instagram_user_info(self, user_id: str) -> dict or None:
        """특정 사용자 정보 조회"""
        try:
            url = f"{self.base_url}/api/ig/user/info"
            params = {
                'ig_id': user_id
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Instagram API 요청 실패: {str(e)}")
            return None

@bp.route('/search', methods=['POST'])
def search_instagram_user_route():
    """
    Instagram 사용자 검색 및 DB 저장
    """
    username = request.json.get('username')
    if not username:
        abort(400, description="Username is required")

    try:
        config = InstagramAPIConfig()
        client = InstagramAPIClient(config)
        service = InstagramService(db.session)
        
        api_response = client.search_instagram_user(username)
        
        if not api_response:
            abort(503, description="Instagram API 호출 실패")
        
        if not api_response.get('result'):
            abort(404, description="사용자를 찾을 수 없습니다")
        
        results = api_response.get('result', [])
        saved_users = []
        
        for result in results:
            if 'user' in result:
                user_data = result['user']
                saved_user = service.insert_instagram_user(user_data)
                
                if saved_user:
                    service.insert_api_search_result(
                        user_id=saved_user.id,
                        status=result.get('status', 'success'),
                        raw_response=result
                    )
                    
                    saved_users.append({
                        'id': saved_user.id,
                        'username': saved_user.username,
                        'full_name': saved_user.full_name,
                        'is_verified': saved_user.is_verified,
                        'is_business': saved_user.is_business,
                        'follower_count': saved_user.follower_count,
                        'following_count': saved_user.following_count,
                        'media_count': saved_user.media_count,
                        'profile_pic_url': saved_user.profile_pic_url,
                        'biography': saved_user.biography,
                    })
        
        return jsonify({
            'status': 'success',
            'total_results': len(saved_users),
            'saved_users': saved_users
        }), 200
    
    except Exception as e:
        logger.error(f"사용자 검색 오류: {str(e)}")
        abort(500, description="서버 오류가 발생했습니다")

@bp.route('/user/<string:username>', methods=['GET'])
def get_instagram_user_route(username: str):
    """
    저장된 Instagram 사용자 정보 조회
    """
    try:
        service = InstagramService(db.session)
        user = service.get_instagram_user(username)
        
        if not user:
            abort(404, description="사용자를 찾을 수 없습니다")
        
        return jsonify({
            'status': 'success',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        logger.error(f"사용자 조회 오류: {str(e)}")
        abort(500, description="서버 오류가 발생했습니다")

@bp.route('/verified-users', methods=['GET'])
def get_verified_users_route():
    """
    인증된 Instagram 사용자 목록 조회
    """
    limit = request.args.get('limit', 100, type=int)
    if not (1 <= limit <= 1000):
        abort(400, description="Limit must be between 1 and 1000")

    try:
        service = InstagramService(db.session)
        users = service.get_verified_users(limit)
        
        users_data = [
            {
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'follower_count': user.follower_count,
                'is_business': user.is_business,
                'profile_pic_url': user.profile_pic_url
            } for user in users
        ]
        
        return jsonify({
            'status': 'success',
            'total': len(users_data),
            'users': users_data
        }), 200
    
    except Exception as e:
        logger.error(f"사용자 목록 조회 오류: {str(e)}")
        abort(500, description="서버 오류가 발생했습니다")

@bp.route('/business-users', methods=['GET'])
def get_business_users_route():
    """
    비즈니스 계정 목록 조회
    """
    limit = request.args.get('limit', 100, type=int)
    if not (1 <= limit <= 1000):
        abort(400, description="Limit must be between 1 and 1000")

    try:
        service = InstagramService(db.session)
        users = service.get_business_users(limit)
        
        users_data = [
            {
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'follower_count': user.follower_count,
                'is_verified': user.is_verified,
                'profile_pic_url': user.profile_pic_url,
                'external_url': user.external_url,
                'biography': user.biography
            } for user in users
        ]
        
        return jsonify({
            'status': 'success',
            'total': len(users_data),
            'users': users_data
        }), 200
    
    except Exception as e:
        logger.error(f"비즈니스 사용자 목록 조회 오류: {str(e)}")
        abort(500, description="서버 오류가 발생했습니다")

@bp.route('/search-by-followers', methods=['GET'])
def search_by_follower_count_route():
    """
    팔로워 수 범위로 사용자 검색
    """
    min_followers = request.args.get('min_followers', 0, type=int)
    max_followers = request.args.get('max_followers', type=int)
    limit = request.args.get('limit', 100, type=int)

    if not (1 <= limit <= 1000):
        abort(400, description="Limit must be between 1 and 1000")
    if min_followers < 0:
        abort(400, description="Min followers cannot be negative")
    if max_followers is not None and max_followers < 0:
        abort(400, description="Max followers cannot be negative")
    if max_followers is not None and min_followers > max_followers:
        abort(400, description="Min followers cannot be greater than max followers")

    try:
        service = InstagramService(db.session)
        users = service.search_users_by_follower_count(
            min_followers=min_followers,
            max_followers=max_followers,
            limit=limit
        )
        
        users_data = [
            {
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'follower_count': user.follower_count,
                'is_verified': user.is_verified,
                'profile_pic_url': user.profile_pic_url,
                'biography': user.biography
            } for user in users
        ]
        
        return jsonify({
            'status': 'success',
            'total': len(users_data),
            'filters': {
                'min_followers': min_followers,
                'max_followers': max_followers
            },
            'users': users_data
        }), 200
    
    except Exception as e:
        logger.error(f"사용자 검색 오류: {str(e)}")
        abort(500, description="서버 오류가 발생했습니다")

@bp.route('/refresh/<string:username>', methods=['POST'])
def refresh_user_data_route(username: str):
    """
    특정 사용자의 Instagram 정보 새로고침
    """
    try:
        service = InstagramService(db.session)
        user = service.get_instagram_user(username)
        
        if not user:
            abort(404, description="사용자를 찾을 수 없습니다")
        
        config = InstagramAPIConfig()
        client = InstagramAPIClient(config)
        api_response = client.search_instagram_user(username)
        
        if not api_response or not api_response.get('result'):
            abort(503, description="Instagram API 호출 실패")
        
        for result in api_response.get('result', []):
            if 'user' in result:
                updated_user = service._update_instagram_user(user, result['user'])
                
                return jsonify({
                    'status': 'success',
                    'message': '사용자 정보가 업데이트되었습니다',
                    'user': {
                        'id': updated_user.id,
                        'username': updated_user.username,
                        'follower_count': updated_user.follower_count,
                        'following_count': updated_user.following_count,
                        'media_count': updated_user.media_count,
                        'updated_at': updated_user.updated_at.isoformat() if updated_user.updated_at else None
                    }
                }), 200
        
        abort(500, description="사용자 정보 업데이트 실패")
    
    except Exception as e:
        logger.error(f"사용자 새로고침 오류: {str(e)}")
        abort(500, description="서버 오류가 발생했습니다")


