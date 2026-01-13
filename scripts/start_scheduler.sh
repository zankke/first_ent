#!/bin/bash

# 뉴스 크롤링 스케줄러 시작 스크립트
cd /Users/veritas-macbookpro/Documents/work/first_ent/backend

# 가상환경 활성화
source venv/bin/activate

# 환경변수 설정
export FLASK_APP=app
export FLASK_ENV=development

# 스케줄러 시작
python -c "
from services.scheduler import news_scheduler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('뉴스 크롤링 스케줄러를 시작합니다...')
news_scheduler.start_scheduler()

# 스케줄러가 계속 실행되도록 대기
import time
try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    logger.info('스케줄러를 중지합니다...')
    news_scheduler.stop_scheduler()
"


