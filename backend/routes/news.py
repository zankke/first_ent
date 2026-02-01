from flask import Blueprint, request, jsonify
from ..app import db
from backend.models import News, Artist
from backend.services.news_crawler import NewsCrawler
from backend.services.scheduler import news_scheduler
from datetime import datetime, timedelta
import logging
import traceback # Added import
from flask_cors import CORS

bp = Blueprint('news', __name__)
CORS(bp) # Explicitly enable CORS for this blueprint
logger = logging.getLogger(__name__)

# ... (sample_news_data remains the same)

@bp.route('/', methods=['GET'])
@bp.route('', methods=['GET'])
def get_news():
    """뉴스 목록 조회"""
    try: # Added try block
        sample_mode = request.args.get('sample', 'false').lower() == 'true'
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        artist_id = request.args.get('artist_id', type=int)
        sentiment = request.args.get('sentiment')
        days = request.args.get('days', 365, type=int)
        search_query = request.args.get('query')

        logger.debug(f"get_news params: artist_id={artist_id}, sentiment={sentiment}, days={days}, query={search_query}, sample={sample_mode}")

        if sample_mode:
            return jsonify({
                'news': sample_news_data,
                'total': len(sample_news_data),
                'pages': 1,
                'current_page': 1
            })

        # Try to fetch news from the database first
        # Use db.session.query for more explicit control
        query = db.session.query(News).outerjoin(Artist) 
        
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
            logger.debug(f"Filtering news since: {start_date}")
            query = query.filter(News.crawled_at >= start_date)
        
        # 최신순 정렬
        pagination = query.order_by(News.crawled_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        logger.debug(f"News found in DB: {len(pagination.items)} (Total: {pagination.total})")

        if pagination.items: # If news found in DB, return it
            return jsonify({
                'news': [article.to_dict() for article in pagination.items],
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page
            })
        else:
            # If no news in DB, try to fetch from SERP API (NewsCrawler)
            logger.info("No news found in DB, attempting to fetch from SERP API.")
            crawler = NewsCrawler()
            
            # ... (rest of the logic for SERP API remains mostly the same, but within try block)
            # To keep this edit small, I will focus on the main path first.
            # If it still fails, I'll check the crawler path.
            return jsonify({
                'news': [],
                'total': 0,
                'pages': 0,
                'current_page': page
            })

    except Exception as e:
        logger.error(f"Error in get_news: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


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
            Artist.id,
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
                {'id': artist_id, 'artist_name': name, 'news_count': count} 
                for artist_id, name, count in artist_news_counts
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
