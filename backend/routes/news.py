from flask import Blueprint, request, jsonify
from ..app import db
from backend.models import News, Artist
from backend.services.news_crawler import NewsCrawler
from backend.services.scheduler import news_scheduler
from datetime import datetime, timedelta
import logging
from flask_cors import CORS

bp = Blueprint('news', __name__)
CORS(bp) # Explicitly enable CORS for this blueprint
logger = logging.getLogger(__name__)

# Sample news data for fallback or example display
sample_news_data = [
    {
        "id": 999999999,
        "artist_id": 1, # Assuming artist with ID 1 exists
        "artist_name": "박서준",
        "title": "[샘플] 박서준, 새 드라마 \'화랑\'으로 안방극장 복귀 예정",
        "content": "배우 박서준이 KBS2 새 월화드라마 \'화랑\'으로 안방극장에 복귀한다. \'화랑\'은 신라 시대를 배경으로 화랑들의 뜨거운 열정과 사랑, 성장을 그리는 청춘 드라마로, 박서준은 극 중 전설적인 화랑 \'무명\' 역을 맡아...",
        "url": "https://sample-news.com/park-seo-joon-hwarang",
        "source": "샘플 미디어",
        "published_at": datetime.now().isoformat(),
        "crawled_at": datetime.now().isoformat(),
        "sentiment": "positive",
        "relevance_score": 0.95,
        "keywords": ["박서준", "화랑", "드라마"],
        "thumbnail": "https://picsum.photos/seed/sample/200/200",
        "media_name": "샘플 미디어 아울렛"
    },
    {
        "id": 999999998,
        "artist_id": 1, # Assuming artist with ID 1 exists
        "artist_name": "박서준",
        "title": "[샘플] 박서준, 칸 영화제 참석... 글로벌 행보 이어가",
        "content": "배우 박서준이 제78회 칸 국제 영화제에 참석하여 레드카펫을 밟았다. 그는 주연을 맡은 영화 \'드림\'이 비경쟁 부문에 초청되어...",
        "url": "https://sample-news.com/park-seo-joon-cannes",
        "source": "글로벌 연예",
        "published_at": (datetime.now() - timedelta(days=1)).isoformat(),
        "crawled_at": (datetime.now() - timedelta(days=1)).isoformat(),
        "sentiment": "neutral",
        "relevance_score": 0.80,
        "keywords": ["박서준", "칸 영화제", "글로벌"],
        "thumbnail": "https://picsum.photos/seed/sample2/200/200",
        "media_name": "글로벌 연예"
    }
]

@bp.route('/', methods=['GET'])
@bp.route('', methods=['GET'])
def get_news():
    """뉴스 목록 조회"""
    sample_mode = request.args.get('sample', 'false').lower() == 'true'
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    artist_id = request.args.get('artist_id', type=int)
    sentiment = request.args.get('sentiment')
    days = request.args.get('days', 365, type=int)
    search_query = request.args.get('query')

    if sample_mode:
        return jsonify({
            'news': sample_news_data,
            'total': len(sample_news_data),
            'pages': 1,
            'current_page': 1
        })

    # Try to fetch news from the database first
    query = News.query.join(Artist) # Join with Artist model
    
    if artist_id:
        query = query.filter(News.artist_id == artist_id)
    
    if sentiment:
        query = query.filter(News.sentiment == sentiment)
    
    if search_query:
        search_pattern = f'%{search_query}%'
        query = query.filter(
            db.or_(
                News.title.ilike(search_pattern),
                News.content.ilike(search_pattern),
                Artist.name.ilike(search_pattern)
            )
        )
    
    # 날짜 필터링
    if days:
        start_date = datetime.utcnow() - timedelta(days=days)
        query = query.filter(News.crawled_at >= start_date)
    
    # 최신순 정렬
    news_from_db = query.order_by(News.crawled_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    if news_from_db.items: # If news found in DB, return it
        return jsonify({
            'news': [article.to_dict() for article in news_from_db.items],
            'total': news_from_db.total,
            'pages': news_from_db.pages,
            'current_page': page
        })
    else:
        # If no news in DB, try to fetch from SERP API (NewsCrawler)
        logger.info("No news found in DB, attempting to fetch from SERP API.")
        crawler = NewsCrawler()
        fetched_news_items = []
        
        # Determine which artist to search for
        artist_to_search = None
        if artist_id:
            artist_to_search = Artist.query.get(artist_id)
        elif search_query: # If artist_id is not provided, try to find artist by search_query
            artist_to_search = Artist.query.filter(Artist.name.ilike(f'%{search_query}%')).first()
        
        if artist_to_search:
            logger.info(f"Attempting to fetch news for artist: {artist_to_search.name} from SERP API.")
            fetched_news_items = crawler.search_news_for_artist(artist_to_search, days_back=days)
            
            if fetched_news_items:
                logger.info(f"Successfully fetched {len(fetched_news_items)} news items for {artist_to_search.name} from SERP API. Saving to DB.")
                crawler.save_news_to_db(fetched_news_items, artist_to_search)
                # Re-query from DB to get full News objects with IDs etc.
                news_from_db = query.order_by(News.crawled_at.desc()).paginate(
                    page=page, per_page=per_page, error_out=False
                )
                return jsonify({
                    'news': [article.to_dict() for article in news_from_db.items],
                    'total': news_from_db.total,
                    'pages': news_from_db.pages,
                    'current_page': page
                })
            else:
                logger.warning(f"SERP API returned no news items for {artist_to_search.name} or failed to fetch.")
        else:
            logger.warning("No specific artist to search for in SERP API.")
            
        logger.warning("Failed to fetch news from SERP API or no artist specified, returning sample news.")
        return jsonify({
            'news': sample_news_data,
            'total': len(sample_news_data),
            'pages': 1,
            'current_page': 1
        })

@bp.route('/<int:news_id>', methods=['GET'])
def get_news_article(news_id):
    """특정 뉴스 기사 조회"""
    article = News.query.get_or_404(news_id)
    return jsonify(article.to_dict())

@bp.route('/artist/<int:artist_id>', methods=['GET'])
def get_news_by_artist(artist_id):
    """특정 아티스트의 뉴스 조회"""
    artist = Artist.query.get_or_404(artist_id)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    days = request.args.get('days', 30, type=int)
    
    query = News.query.filter_by(artist_id=artist_id)
    
    # 날짜 필터링
    if days:
        start_date = datetime.utcnow() - timedelta(days=days)
        query = query.filter(News.crawled_at >= start_date)
    
    news = query.order_by(News.crawled_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'artist': artist.to_dict(),
        'news': [article.to_dict() for article in news.items],
        'total': news.total,
        'pages': news.pages,
        'current_page': page
    })

@bp.route('/crawl', methods=['POST'])
def crawl_news():
    """수동으로 뉴스 크롤링 실행"""
    try:
        artist_id = request.json.get('artist_id') if request.json else None
        
        crawler = NewsCrawler()
        
        if artist_id:
            # 특정 아티스트만 크롤링
            artist = Artist.query.get_or_404(artist_id)
            news_items = crawler.search_news_for_artist(artist)
            saved_count = crawler.save_news_to_db(news_items, artist)
            
            return jsonify({
                'message': f'{artist.name}에 대한 뉴스 크롤링이 완료되었습니다.',
                'artist_name': artist.name,
                'saved_count': saved_count
            })
        else:
            # 모든 아티스트 크롤링
            results = crawler.crawl_news_for_all_artists()
            total_news = sum(results.values())
            
            return jsonify({
                'message': '모든 아티스트에 대한 뉴스 크롤링이 완료되었습니다.',
                'results': results,
                'total_news': total_news
            })
            
    except Exception as e:
        logger.error(f"뉴스 크롤링 중 오류: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/scheduler/status', methods=['GET'])
def get_scheduler_status():
    """스케줄러 상태 조회"""
    return jsonify({
        'is_running': news_scheduler.is_running,
        'next_run_time': news_scheduler.get_next_run_time()
    })

@bp.route('/scheduler/start', methods=['POST'])
def start_scheduler():
    """스케줄러 시작"""
    try:
        news_scheduler.start_scheduler()
        return jsonify({
            'message': '뉴스 크롤링 스케줄러가 시작되었습니다.',
            'next_run_time': news_scheduler.get_next_run_time()
        })
    except Exception as e:
        logger.error(f"스케줄러 시작 중 오류: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/scheduler/stop', methods=['POST'])
def stop_scheduler():
    """스케줄러 중지"""
    try:
        news_scheduler.stop_scheduler()
        return jsonify({'message': '뉴스 크롤링 스케줄러가 중지되었습니다.'})
    except Exception as e:
        logger.error(f"스케줄러 중지 중 오류: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/scheduler/run', methods=['POST'])
def run_scheduler_manual():
    """수동으로 스케줄러 실행"""
    try:
        news_scheduler.run_manual_crawl()
        return jsonify({'message': '수동 뉴스 크롤링이 실행되었습니다.'})
    except Exception as e:
        logger.error(f"수동 크롤링 실행 중 오류: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/stats', methods=['GET'])
def get_news_stats():
    """뉴스 통계 조회"""
    try:
        # 전체 뉴스 수
        total_news = News.query.count()
        
        # 최근 7일간 뉴스 수
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_news = News.query.filter(News.crawled_at >= week_ago).count()
        
        # 아티스트별 뉴스 수
        artist_news_counts = db.session.query(
            Artist.name,
            db.func.count(News.id).label('news_count')
        ).join(News).group_by(Artist.id, Artist.name).all()
        
        # 감정별 뉴스 수
        sentiment_counts = db.session.query(
            News.sentiment,
            db.func.count(News.id).label('count')
        ).group_by(News.sentiment).all()
        
        return jsonify({
            'total_news': total_news,
            'recent_news': recent_news,
            'artist_news_counts': [
                {'artist_name': name, 'news_count': count} 
                for name, count in artist_news_counts
            ],
            'sentiment_counts': [
                {'sentiment': sentiment, 'count': count} 
                for sentiment, count in sentiment_counts
            ]
        })
        
    except Exception as e:
        logger.error(f"뉴스 통계 조회 중 오류: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    """뉴스 기사 삭제"""
    article = News.query.get_or_404(news_id)
    db.session.delete(article)
    db.session.commit()
    
    return jsonify({'message': '뉴스 기사가 삭제되었습니다.'}), 200

@bp.route('/<int:news_id>/sentiment', methods=['PUT'])
def update_sentiment(news_id):
    """뉴스 기사의 감정 분석 결과 업데이트"""
    article = News.query.get_or_404(news_id)
    data = request.get_json()
    
    sentiment = data.get('sentiment')
    if sentiment not in ['positive', 'negative', 'neutral']:
        return jsonify({'error': '유효하지 않은 감정 값입니다.'}), 400
    
    article.sentiment = sentiment
    article.relevance_score = data.get('relevance_score', article.relevance_score)
    article.is_processed = True
    
    db.session.commit()
    
    return jsonify(article.to_dict())
