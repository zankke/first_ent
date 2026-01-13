#!/usr/bin/env python3
"""
뉴스 크롤링 기능 + DB 삽입 기능 간단 테스트
"""

import sys
import os

# backend 모듈 경로를 PYTHONPATH에 추가 (docker·로컬 어느 경로든)
BACKEND_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)

import logging

try:
    from app import create_app
    from services.news_crawler import NewsCrawler
    from models import Artist
except ModuleNotFoundError as e:
    print("❌ backend 모듈 또는 의존성이 누락되었습니다.")
    print("- backend, scripts 폴더의 상대 위치가 맞는지 확인하세요.")
    print("- python scripts/test_news_crawler.py 형태로 실행해야 합니다.")
    print(f"상세오류: {e}")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_news_crawler():
    """뉴스 크롤러가 정상 작동하는지 확인"""
    app = create_app()
    with app.app_context():
        # Test artist 생성 또는 조회 (이름, DB에 없는 경우 새로 삽입)
        artist = Artist.query.filter_by(name='소지섭').first()
        if not artist:
            artist = Artist(
                name='소지섭',
                real_name='소지섭',
                nationality='Korea',
                agency='Test Agency',
                status='active'
            )
            try:
                from app import db
            except ImportError:
                from backend.app import db
            db.session.add(artist)
            db.session.commit()
            logger.info("테스트 아티스트 '소지섭'을 새로 생성했습니다.")
        else:
            logger.info(f"기존 테스트 아티스트 발견: {artist.name}")

        # 크롤러 인스턴스
        crawler = NewsCrawler()
        logger.info(f"{artist.name}의 최신 뉴스 크롤링 시도...")

        try:
            news_items = crawler.search_news_for_artist(artist)
            logger.info(f"검색된 뉴스 개수: {len(news_items)}")
            saved_count = crawler.save_news_to_db(news_items, artist)
            logger.info(f"DB에 저장된 뉴스 개수: {saved_count}")

            try:
                from models import News
            except ImportError:
                from backend.models import News

            saved_news = News.query.filter_by(artist_id=artist.id).order_by(News.published_at.desc()).all()
            logger.info(f"DB에 저장된 총 뉴스: {len(saved_news)}")

            for idx, news in enumerate(saved_news[:3]):
                logger.info(f"{idx+1}. {news.title}\n    URL: {news.url}\n    출처: {news.source}\n    발행일: {news.published_at}\n---")

        except Exception as err:
            logger.error(f"뉴스 크롤링 또는 저장 중 오류: {err}")
            return False
        logger.info("✅ 뉴스 크롤러 단일 테스트 완료")
        return True

if __name__ == "__main__":
    print("=== 뉴스 크롤러 기능 & DB 연결 테스트 시작 ===")
    print("✔ Perplexity API KEY가 반드시 환경 변수에 등록되어 있어야 합니다.")
    print()
    try:
        success = test_news_crawler()
        print()
        if success:
            print("🎉 테스트 성공: 크롤링 및 DB 저장 OK")
            sys.exit(0)
        else:
            print("❌ 테스트 실패 - backend 모듈·DB·API 키 환경 등을 확인하세요.")
            sys.exit(1)
    except ModuleNotFoundError as e:
        print("❌ backend 모듈 또는 의존성이 누락되었습니다.")
        print("- backend, scripts 폴더의 상대 위치가 맞는지 확인하세요.")
        print("- 반드시 python scripts/test_news_crawler.py 형태로 실행해야 합니다.")
        print(f"상세오류: {e}")
        sys.exit(1)
    except Exception as ex:
        print("❌ 예기치 못한 오류 발생!")
        print(f"상세오류: {ex}")
        sys.exit(1)
