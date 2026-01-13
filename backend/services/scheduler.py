# backend/services/scheduler.py

import schedule
import threading
import time
import logging

logger = logging.getLogger(__name__)

class NewsScheduler:
    def __init__(self):
        self.app = None
        self.is_running = False
        self.scheduler_thread = None

    def init_app(self, app):
        """Flask 앱을 외부에서 주입받음"""
        self.app = app

    def crawl_news_job(self):
        if not self.app:
            logger.error("Flask app is not initialized in NewsScheduler.")
            return

        with self.app.app_context():
            logger.info("[스케줄러] 뉴스 크롤링 시작...")
            # 실제 뉴스 크롤링 함수 호출
            # e.g., fetch_news_for_all_artists()
            logger.info("[스케줄러] 뉴스 크롤링 완료.")

    def start_scheduler(self):
        if self.is_running:
            logger.warning("스케줄러가 이미 실행 중입니다.")
            return

        schedule.every().day.at("05:00").do(self.crawl_news_job)

        self.is_running = True

        def run_scheduler():
            logger.info("뉴스 크롤링 스케줄러 실행 시작 (백그라운드)")
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)

        self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()

    def stop_scheduler(self):
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        logger.info("스케줄러가 중지되었습니다.")

    def run_manual_crawl(self):
        logger.info("수동 뉴스 크롤링 실행...")
        self.crawl_news_job()

    def get_next_run_time(self):
        """다음 스케줄된 실행 시간을 반환합니다."""
        if schedule.next_run():
            return schedule.next_run().strftime("%Y-%m-%d %H:%M:%S")
        return "N/A"

# 전역 인스턴스
news_scheduler = NewsScheduler()