import requests
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from backend.app import db
from backend.models import News, Artist, APIKey
import logging

logger = logging.getLogger(__name__)

class NewsCrawler:
    def __init__(self):
        self.serpapi_api_key = os.getenv('SERPAPI_API_KEY') # Assuming SERPAPI API key is in .env
        
    def get_serpapi_api_key(self) -> Optional[str]:
        """SERP API 키를 DB에서 가져오기"""
        api_key = APIKey.query.filter_by(
            platform='serpapi',
            is_active=True
        ).first()
        
        if api_key:
            return api_key.api_key
        
        # 환경변수에서 가져오기
        return self.serpapi_api_key
    
    def search_news_for_artist(self, artist: Artist, days_back: int = 7) -> List[Dict]:
        """특정 아티스트에 대한 뉴스 검색 (SERP API 사용)"""
        api_key = self.get_serpapi_api_key()
        if not api_key:
            logger.error("SERP API 키를 찾을 수 없습니다.")
            return []
        
        from serpapi import GoogleSearch

        # 검색 쿼리 구성
        query = f"{artist.name}"
        
        params = {
            "api_key": api_key,
            "engine": "google",
            "q": query,
            "tbm": "nws",
            "gl": "kr",
            "hl": "ko",
            "num": 10
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            if "news_results" in results:
                return self._parse_serpapi_response(results['news_results'], artist)
            else:
                logger.warning(f"No news results found for {artist.name}")
                return []
        except Exception as e:
            logger.error(f"SERP API 요청 중 오류 발생: {str(e)}")
            return []
    
    def _parse_serpapi_response(self, response_data: List[Dict], artist: Artist) -> List[Dict]:
        """SERP API 응답을 파싱하여 뉴스 데이터 추출"""
        news_items = []
        for item in response_data:
            logger.debug(f"Parsing SerpApi item: {json.dumps(item, indent=2)}")
            title = item.get('title', '')
            link = item.get('link', '')
            snippet = item.get('snippet', '')
            source = item.get('source', '')
            published_at = item.get('date', '') # SerpApi uses 'date' for published date
            thumbnail = item.get('thumbnail', '') # Assuming thumbnail is available
            
            # Trim content to 150 characters
            trimmed_content = (snippet[:150] + '...') if len(snippet) > 150 else snippet

            news_items.append(self._create_news_item({
                'title': title,
                'content': trimmed_content,
                'url': link,
                'source': source,
                'published_at': published_at,
                'thumbnail': thumbnail,
                'media_name': source
            }, artist))
        return news_items
    
    def _create_news_item(self, item: Dict, artist: Artist) -> Dict:
        """뉴스 아이템 생성"""
        logger.debug(f"Creating news item from: {json.dumps(item, indent=2)}")
        return {
            'thumbnail': item.get('thumbnail', ''),
            'media_name': item.get('media_name', ''),
            'title': item.get('title', ''),
            'content': item.get('content', ''),
            'url': item.get('url', ''),
            'source': item.get('source', ''), 
            'published_at': self._parse_published_date(item.get('published_at', '')),
            'keywords': [artist.name]
        }
    
    def _parse_published_date(self, date_str: str) -> Optional[datetime]:
        """발행일 문자열을 datetime으로 변환"""
        logger.debug(f"Attempting to parse date_str: '{date_str}'")
        if not date_str:
            logger.debug("date_str is empty, returning None.")
            return None
        
        try:
            # 다양한 날짜 형식 처리
            date_formats = [
                '%Y-%m-%d',
                '%Y-%m-%d %H:%M:%S',
                '%Y년 %m월 %d일',
                '%m월 %d일',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%dT%H:%M:%SZ',
                '%Y. %m. %d.'
            ]
            
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    logger.debug(f"Successfully parsed '{date_str}' with format '{fmt}' to {parsed_date}")
                    return parsed_date
                except ValueError:
                    continue
            
            # Relative date parsing
            if '일 전' in date_str or '주 전' in date_str or '시간 전' in date_str:
                now = datetime.now()
                if '일 전' in date_str:
                    days = int(date_str.split('일 전')[0])
                    parsed_date = now - timedelta(days=days)
                    logger.debug(f"Parsed relative date '{date_str}' to {parsed_date}")
                    return parsed_date
                elif '주 전' in date_str:
                    weeks = int(date_str.split('주 전')[0])
                    parsed_date = now - timedelta(weeks=weeks)
                    logger.debug(f"Parsed relative date '{date_str}' to {parsed_date}")
                    return parsed_date
                elif '시간 전' in date_str:
                    hours = int(date_str.split('시간 전')[0])
                    parsed_date = now - timedelta(hours=hours)
                    logger.debug(f"Parsed relative date '{date_str}' to {parsed_date}")
                    return parsed_date
            
            logger.warning(f"Failed to parse date_str: '{date_str}' with any known format or relative pattern.")
            return None
        except Exception as e:
            logger.error(f"Error parsing date_str '{date_str}': {e}", exc_info=True)
            return None
    
    def save_news_to_db(self, news_items: List[Dict], artist: Artist) -> int:
        """뉴스를 데이터베이스에 저장"""
        saved_count = 0
        
        for item in news_items:
            try:
                # 중복 확인 (URL 기준)
                existing_news = News.query.filter_by(
                    artist_id=artist.id,
                    url=item['url']
                ).first()
                
                if existing_news:
                    continue
                
                news = News(
                    artist_id=artist.id,
                    title=item['title'],
                    content=item['content'],
                    url=item['url'],
                    source=item.get('source', ''),
                    published_at=item['published_at'],
                    keywords=item.get('keywords', []),
                    thumbnail=item.get('thumbnail', ''),
                    media_name=item.get('media_name', '')
                )
                
                db.session.add(news)
                saved_count += 1
                
            except Exception as e:
                logger.error(f"뉴스 저장 중 오류: {str(e)}")
                continue
        
        try:
            db.session.commit()
            logger.info(f"{artist.name}에 대한 {saved_count}개의 뉴스가 저장되었습니다.")
        except Exception as e:
            logger.error(f"데이터베이스 커밋 중 오류: {str(e)}")
            db.session.rollback()
            saved_count = 0
        
        return saved_count
    
    def crawl_news_for_all_artists(self) -> Dict[str, int]:
        """모든 활성 아티스트에 대한 뉴스 크롤링"""
        results = {}
        
        # 활성 상태인 아티스트들 조회
        active_artists = Artist.query.filter_by(status='active').all()
        
        for artist in active_artists:
            try:
                logger.info(f"{artist.name}에 대한 뉴스 크롤링 시작...")
                news_items = self.search_news_for_artist(artist)
                saved_count = self.save_news_to_db(news_items, artist)
                results[artist.name] = saved_count
                logger.info(f"{artist.name}: {saved_count}개 뉴스 저장 완료")
            except Exception as e:
                logger.error(f"{artist.name} 뉴스 크롤링 중 오류: {str(e)}")
                results[artist.name] = 0
        
        return results
