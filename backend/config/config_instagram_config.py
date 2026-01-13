# config/instagram_config.py
"""
Instagram API 설정
"""

import os
from dotenv import load_dotenv

load_dotenv()


class InstagramAPIConfig:
    """Instagram API 설정 클래스"""
    
    # RapidAPI 설정
    BASE_URL: str = os.getenv(
        'INSTAGRAM_API_BASE_URL',
        'https://instagram-api-extended.p.rapidapi.com'
    )
    
    RAPIDAPI_HOST: str = os.getenv(
        'INSTAGRAM_RAPIDAPI_HOST',
        'instagram-api-extended.p.rapidapi.com'
    )
    
    RAPIDAPI_KEY: str = os.getenv(
        'INSTAGRAM_RAPIDAPI_KEY',
        ''  # RapidAPI 키를 환경변수에서 설정해야 함
    )
    
    # API 설정
    TIMEOUT: int = int(os.getenv('INSTAGRAM_API_TIMEOUT', '10'))
    RETRY_COUNT: int = int(os.getenv('INSTAGRAM_API_RETRY_COUNT', '3'))
    RETRY_DELAY: int = int(os.getenv('INSTAGRAM_API_RETRY_DELAY', '2'))
    
    # 데이터베이스 설정
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', '3306'))
    DB_USER: str = os.getenv('DB_USER', 'root')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
    DB_NAME: str = os.getenv('DB_NAME', 'instagram_db')
    
    # 로깅 설정
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'logs/instagram_api.log')
    
    # 캐시 설정
    CACHE_ENABLED: bool = os.getenv('CACHE_ENABLED', 'True').lower() == 'true'
    CACHE_TTL: int = int(os.getenv('CACHE_TTL', '3600'))  # 1시간
    
    # 레이트 제한 설정
    RATE_LIMIT_ENABLED: bool = os.getenv('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_REQUESTS: int = int(os.getenv('RATE_LIMIT_REQUESTS', '100'))
    RATE_LIMIT_WINDOW: int = int(os.getenv('RATE_LIMIT_WINDOW', '3600'))  # 1시간
    
    @classmethod
    def validate(cls) -> bool:
        """설정 유효성 검증"""
        if not cls.RAPIDAPI_KEY:
            raise ValueError("INSTAGRAM_RAPIDAPI_KEY 환경변수를 설정해주세요")
        return True
    
    @classmethod
    def get_db_url(cls) -> str:
        """데이터베이스 연결 URL 반환"""
        return f"mysql+pymysql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}?charset=utf8mb4"
