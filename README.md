지금부터 'AI 기반 Aritist 관리 프레임워크'를 만드는 내부 프로젝트를 킥오프합니다. 소속된 아티스트의 정보를 등록/관리/조회하는 내부 시스템입니다. 첨부 파일을 깊게 분석한 후 시스템 개발에 필요한 Database Schema를 정의하고, 그 이유를 설명하세요. 아래 요구 조건을 참고해 프로젝트 환경 구성에 필요한 init_project.sh 파일을 생성해 주세요. 

[Architecture] 
* Dev_Environment : MacOS M2 PRO(ARM)
* Frontend: Streamlit, streamlit_antd_components, TailwindCSS, bootstrap
* Backend : Python, Streamlit, streamlit_antd_components
* Database : MySQL (Docker container port 3307 : Database > first_ent) 
* Project_Root_Path : /Users/veritas-macbookpro/Documents/work/first_ent_new

[주요기능]
1) 모델 정보 
  - 정보 등록 | 조회 | 수정 
  - 채널 정보 등록 | 관리 
 (Instagram) get instagram channel info (id/follower/following/posts) 
 (Youtube) get channel info  
2) Account 관리 
3) 게시판 관리 : 신규 생성 | 수정 
4) Databse 관리 : 커넥션 정보 등록 / 수정
5) API 관리 
 (Instagram) rapid_api : get channel info API 
 (Youtube api) get channel info API
6) 뉴스 & 미디어 관리 :
- Perplexity API를 이용해, 선택된 모델에 대한 관련 뉴스를 매일 오전 05시 기준으로 크롤링 하고 DB에저장한 후, 해당 아티스트 정보 페이지 하단에 표시하는 기능 추가
7) 그 외 필요한 기능을 제안하세요 

[UI/UX] 
• TailwindCSS, Shadcdn을 적극 활용
• 세계 최고 수준의 상업용 전문 소프트웨어처럼 보이도록 룩앤필과 UI를 구현해 주세요.
• 최대한 심플한 5개 이하의 컬러 코드 이내에서 구성하세요  


## Database Schema
: 컨벤션 룰을 사용해 Schema name을 표준화 하세요. 
- **artists**: 아티스트 기본 정보
- **channels**: 소셜미디어 채널 정보 (Instagram, YouTube 등)
- **accounts**: 시스템 사용자 계정
- **boards**: 게시판 관리
- **api_keys**: API 키 관리
- **database_configs**: DB 연결 설정
- **channel_stats**: 채널 통계 데이터
- **posts**: 게시물 정보

## 주요 기능
1. 아티스트 정보 등록/관리/조회
2. 소셜미디어 채널 연동 및 통계 수집
3. **뉴스 모니터링**: Perplexity API를 이용한 자동 뉴스 크롤링
4. 계정 관리 시스템
5. 게시판 관리
6. API 키 관리
7. 데이터베이스 설정 관리

## 뉴스 모니터링 기능
- **자동 크롤링**: 매일 오전 5시에 활성 아티스트에 대한 뉴스 자동 수집
- **Perplexity API**: 고품질 뉴스 검색 및 분석
- **감정 분석**: 뉴스의 긍정/부정/중립 감정 분석
- **관련도 점수**: 아티스트와의 관련도 점수 계산
- **실시간 모니터링**: 웹 인터페이스를 통한 실시간 뉴스 확인
- **필터링**: 아티스트, 감정, 기간별 필터링 지원


[디자인 포인트]
* 글로벌 배경: 고급스러운 딥 네이비 원근 그라디언트, 버튼은 Orange 계열, 가독성이 높은 UI
* 컴포넌트: shadcn/ui 패턴(rounded-2xl, muted/foreground 스케일, focus ring)
* 피드백: sonner 토스트로 성공/오류 상태 즉각 안내

[GUIDE] 
1. 정확한 프로젝트 생성을 위해 사용자가 정의하거나 제공해야 할 내용이 있다면, 프로젝트를 생성하기 전에 먼저 요청하세요
2. 프로젝트 루트에 파일 또는 폴더가 없는 경우, 프로젝트 폴더 트리를 생성하는 Shell Script(init_project.sh)부터 시작하세요. 만약 파일 또는 폴더가 존재한다면 이를 기준으로 업데이트 하는 Step-by-Step Guide를 제시하세요. 
3. CWD는 ‘/Users/veritas-macbookpro/Documents/first_ent’입니다. 기존에 생성된 프로젝트, 컨테이너, 모듈이 있는지 체크하는 것을 잊지 마세요.: 
4. 코드 변경(수정)이 있는 경우, 가능한 한 터미널에서 바로 복붙 후  실행할 수 있는 CMD를 제공하세요. 이때 실행해야 할 파일 및 전체 경로를 정확히 제시하세요. 만약 그렇지 못하는 경우 diff 형태로 제공하세요
5. 생성/수정된 코드를 제시할 때, 현재 코드가 적용될 파일 경로를 반드시 함께 제시해서 사용자 오류 가능성을  미리 방지 하도록 하세요
6. 파일 네이밍은 매우 주의깊게 진행하세요. 최상의 컨벤션 룰을 제안하고 이를 따라 생성하도록 하세요.





## 프로젝트 구조
```
first_ent/
├── backend/                 # Flask/Streamlit 백엔드
│   ├── app/                # Flask 애플리케이션
│   ├── models/             # 데이터베이스 모델
│   ├── routes/             # API 라우트
│   ├── services/           # 비즈니스 로직
│   └── utils/              # 유틸리티 함수
├── frontend/               # React 프론트엔드
│   ├── src/                # 소스 코드
│   └── public/             # 정적 파일
├── database/               # 데이터베이스 관련
│   ├── migrations/         # DB 마이그레이션
│   └── seeds/              # 초기 데이터
├── docker/                 # Docker 설정
├── scripts/                # 실행 스크립트
└── docs/                   # 문서
```

## 설치 및 실행

### 1. Docker 컨테이너 시작
```bash
./scripts/start_docker.sh
```

### 2. Backend 설정
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
./scripts/start_backend.sh
```

### 3. Frontend 설정
```bash
cd frontend
npm install
./scripts/start_frontend.sh
```

### 4. 뉴스 크롤링 스케줄러 설정
```bash
# 환경변수 설정 (backend/.env 파일)
PERPLEXITY_API_KEY=your-perplexity-api-key-here
ENCRYPTION_KEY=your-encryption-key-here

# 스케줄러 시작
./scripts/start_scheduler.sh
```

## Database Schema
- **artists**: 아티스트 기본 정보
- **channels**: 소셜미디어 채널 정보 (Instagram, YouTube 등)
- **accounts**: 시스템 사용자 계정
- **boards**: 게시판 관리
- **api_keys**: API 키 관리
- **database_configs**: DB 연결 설정
- **channel_stats**: 채널 통계 데이터
- **posts**: 게시물 정보

## 주요 기능
1. 아티스트 정보 등록/관리/조회
2. 소셜미디어 채널 연동 및 통계 수집
3. **뉴스 모니터링**: Perplexity API를 이용한 자동 뉴스 크롤링
4. 계정 관리 시스템
5. 게시판 관리
6. API 키 관리
7. 데이터베이스 설정 관리

## 뉴스 모니터링 기능
- **자동 크롤링**: 매일 오전 5시에 활성 아티스트에 대한 뉴스 자동 수집
- **Perplexity API**: 고품질 뉴스 검색 및 분석
- **감정 분석**: 뉴스의 긍정/부정/중립 감정 분석
- **관련도 점수**: 아티스트와의 관련도 점수 계산
- **실시간 모니터링**: 웹 인터페이스를 통한 실시간 뉴스 확인
- **필터링**: 아티스트, 감정, 기간별 필터링 지원
