# INSTAGRAM_INTEGRATION_GUIDE.md
# Instagram API 통합 가이드

## 📋 개요

RapidAPI의 Instagram API를 통해 Instagram 채널 정보를 조회하고, 14개의 정규화된 테이블에 저장하는 완전한 통합 솔루션입니다.

---

## 🚀 빠른 시작

### 1단계: 파일 생성

다음 파일들을 각각의 디렉토리에 생성하세요:

```
backend/
├── models/
│   └── instagram.py                 # ORM 모델 (14개 테이블)
├── routes/
│   └── instagram.py                 # FastAPI 라우트
├── services/
│   └── instagram_service.py          # 비즈니스 로직
├── config/
│   └── instagram_config.py           # 설정 관리
└── .env                              # 환경변수 (프로젝트 루트)
```

### 2단계: 환경변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 RapidAPI 키를 설정하세요:

```env
INSTAGRAM_RAPIDAPI_KEY=your_key_here
INSTAGRAM_RAPIDAPI_HOST=instagram-api-extended.p.rapidapi.com
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=password
DB_NAME=instagram_db
```

### 3단계: 데이터베이스 초기화

```bash
# 데이터베이스 생성
mysql -u root -p -e "CREATE DATABASE instagram_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"

# 테이블 생성 (SQLAlchemy 사용 시)
python -c "
from models.instagram import Base
from config.instagram_config import InstagramAPIConfig
from sqlalchemy import create_engine

engine = create_engine(InstagramAPIConfig.get_db_url())
Base.metadata.create_all(engine)
"
```

### 4단계: 메인 애플리케이션에 라우트 통합

`app/__init__.py` 또는 `main.py`에 다음을 추가하세요:

```python
from fastapi import FastAPI
from routes.instagram import router as instagram_router

app = FastAPI()

# Instagram 라우트 등록
app.include_router(instagram_router)
```

### 5단계: 의존성 설치

```bash
pip install fastapi sqlalchemy pymysql requests python-dotenv
```

---

## 📚 API 엔드포인트

### 1. Instagram 사용자 검색 및 저장

```bash
POST /api/instagram/search?username=bogummy

응답:
{
  "status": "success",
  "total_results": 1,
  "saved_users": [
    {
      "id": 1,
      "username": "bogummy",
      "full_name": "박보검",
      "is_verified": true,
      "is_business": false,
      "follower_count": 3500000,
      "following_count": 1234,
      "media_count": 890,
      "profile_pic_url": "...",
      "biography": "..."
    }
  ]
}
```

### 2. 저장된 사용자 정보 조회

```bash
GET /api/instagram/user/bogummy

응답:
{
  "status": "success",
  "user": {
    "id": 1,
    "username": "bogummy",
    "full_name": "박보검",
    "biography": "Actor, Singer",
    "is_verified": true,
    "is_business": false,
    "follower_count": 3500000,
    "following_count": 1234,
    "media_count": 890,
    "hd_profile_pics": [...],
    "bio_links": [...],
    "business_contacts": [...],
    "created_at": "2025-10-31T09:54:00",
    "updated_at": "2025-10-31T09:54:00"
  }
}
```

### 3. 인증된 사용자 목록

```bash
GET /api/instagram/verified-users?limit=50

응답:
{
  "status": "success",
  "total": 50,
  "users": [...]
}
```

### 4. 비즈니스 계정 목록

```bash
GET /api/instagram/business-users?limit=50

응답:
{
  "status": "success",
  "total": 50,
  "users": [...]
}
```

### 5. 팔로워 수로 검색

```bash
GET /api/instagram/search-by-followers?min_followers=100000&max_followers=500000&limit=50

응답:
{
  "status": "success",
  "total": 50,
  "filters": {
    "min_followers": 100000,
    "max_followers": 500000
  },
  "users": [...]
}
```

### 6. 사용자 정보 새로고침

```bash
POST /api/instagram/refresh/bogummy

응답:
{
  "status": "success",
  "message": "사용자 정보가 업데이트되었습니다",
  "user": {
    "id": 1,
    "username": "bogummy",
    "follower_count": 3500000,
    "following_count": 1234,
    "media_count": 890,
    "updated_at": "2025-10-31T10:00:00"
  }
}
```

---

## 🗄️ 데이터베이스 스키마

### 메인 테이블 (InstagramUsers)
- 75개 컬럼으로 Instagram 사용자의 모든 정보 저장
- PK, 사용자명, 팔로워 수, 인증 여부, 비즈니스 계정 여부 등

### 관련 테이블들
1. **InstagramBusinessContacts**: 비즈니스 연락처
2. **InstagramHDProfilePics**: HD 프로필 사진
3. **InstagramCharityFundraisers**: 자선 펀드레이저
4. **InstagramFanClubs**: 팬 클럽
5. **InstagramBioLinks**: 바이오 링크
6. **InstagramProfileContextLinks**: 프로필 컨텍스트 링크
7. **InstagramProfileContextMutualFollows**: 상호 팔로우
8. **InstagramProfileContextFacepileUsers**: 페이스파일 사용자
9. **InstagramCreatorShoppingInfo**: 크리에이터 쇼핑
10. **InstagramPinnedChannels**: 핀 고정 채널
11. **InstagramAccountBadges**: 계정 배지
12. **InstagramUserPronouns**: 사용자 대명사
13. **InstagramAPISearchResults**: API 조회 기록

---

## 💡 사용 예제

### Python에서 직접 사용

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.instagram_service import InstagramService
from config.instagram_config import InstagramAPIConfig

# 데이터베이스 연결
config = InstagramAPIConfig()
engine = create_engine(config.get_db_url())
Session = sessionmaker(bind=engine)
session = Session()

# 서비스 초기화
service = InstagramService(session)

# 사용자 검색
api_response = {
    'user': {
        'pk': '123456789',
        'username': 'bogummy',
        'full_name': '박보검',
        'is_verified': True,
        'follower_count': 3500000,
        # ... 기타 필드
    }
}

# DB에 저장
user = service.insert_instagram_user(api_response['user'])
print(f"저장된 사용자: {user.username}")

# 사용자 조회
user = service.get_instagram_user('bogummy')
print(f"팔로워: {user.follower_count}")

# 인증된 사용자 검색
verified_users = service.get_verified_users(limit=10)

# 팔로워 수로 검색
popular_users = service.search_users_by_follower_count(
    min_followers=1000000,
    limit=50
)
```

---

## 🔧 문제 해결

### 1. RapidAPI 키 오류
```
ValueError: INSTAGRAM_RAPIDAPI_KEY 환경변수를 설정해주세요
```
**해결책**: `.env` 파일에 `INSTAGRAM_RAPIDAPI_KEY` 설정

### 2. 데이터베이스 연결 오류
```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError)
```
**해결책**: DB 호스트, 사용자, 비밀번호 확인 및 데이터베이스 생성 여부 확인

### 3. API 요청 타임아웃
```
requests.exceptions.ConnectTimeout
```
**해결책**: 네트워크 연결 확인 및 `INSTAGRAM_API_TIMEOUT` 값 증가

---

## 📊 성능 최적화

### 1. 인덱싱
```sql
-- 주요 인덱스는 자동으로 생성됨
-- 추가 인덱스 필요 시:
CREATE INDEX idx_follower_count ON InstagramUsers(follower_count);
CREATE INDEX idx_is_verified_business ON InstagramUsers(is_verified, is_business);
```

### 2. 캐싱
```python
# Redis 캐시 추가 (선택사항)
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_user(username: str):
    return service.get_instagram_user(username)
```

### 3. 배치 작업
```python
# 여러 사용자 한 번에 저장
users = ['bogummy', 'user2', 'user3']
for username in users:
    api_response = client.search_instagram_user(username)
    service.insert_instagram_user(api_response['user'])
```

---

## 🔐 보안 권장사항

1. **환경변수 보호**: `.env` 파일을 `.gitignore`에 추가
2. **API 키 로테이션**: 정기적으로 RapidAPI 키 변경
3. **레이트 제한**: `RATE_LIMIT_ENABLED` 활성화
4. **입력 검증**: 사용자 입력 검증 강화
5. **로깅**: 민감한 정보 로깅 금지

---

## 📝 로깅 설정

```python
import logging
from config.instagram_config import InstagramAPIConfig

# 로깅 설정
logging.basicConfig(
    level=InstagramAPIConfig.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(InstagramAPIConfig.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

---

## 🚀 배포

### Docker 예제

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: instagram_db
    ports:
      - "3306:3306"
  
  backend:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - mysql
    environment:
      - DB_HOST=mysql
      - INSTAGRAM_RAPIDAPI_KEY=${INSTAGRAM_RAPIDAPI_KEY}
```

---

## 📚 참고 자료

- [RapidAPI Instagram API](https://rapidapi.com/restyler/api/instagram-api-extended)
- [SQLAlchemy 문서](https://docs.sqlalchemy.org/)
- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [MySQL 문서](https://dev.mysql.com/doc/)

---

## 💬 지원

문제가 발생하면 로그 파일을 확인하고, 에러 메시지를 참고하세요.
