#!/bin/bash

# AI 기반 Artist Management Framework 프로젝트 초기화 스크립트
# 실행 환경: MacOS M2 PRO (ARM)

set -e

PROJECT_ROOT="/Users/veritas-macbookpro/Documents/work/first_ent"
echo "🚀 AI 기반 Artist Management Framework 프로젝트 초기화를 시작합니다..."

# 프로젝트 루트 디렉토리로 이동
cd "$PROJECT_ROOT"

# 1. 프로젝트 폴더 구조 생성
echo "📁 프로젝트 폴더 구조를 생성합니다..."
mkdir -p backend/{app,models,routes,services,utils,config}
mkdir -p frontend/{src/{components,pages,hooks,utils,types},public}
mkdir -p database/{migrations,seeds}
mkdir -p docker
mkdir -p docs
mkdir -p scripts

# 2. Backend 환경 설정
echo "🐍 Backend 환경을 설정합니다..."
cat > backend/requirements.txt << 'EOF'
Flask==2.3.3
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.5
PyMySQL==1.1.0
python-dotenv==1.0.0
requests==2.31.0
streamlit==1.28.1
pandas==2.1.1
python-dateutil==2.8.2
cryptography==41.0.4
bcrypt==4.0.1
PyJWT==2.8.0
EOF

# 3. Frontend 환경 설정
echo "⚛️ Frontend 환경을 설정합니다..."
cat > frontend/package.json << 'EOF'
{
  "name": "artist-management-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.15.0",
    "@radix-ui/react-accordion": "^1.1.2",
    "@radix-ui/react-alert-dialog": "^1.0.5",
    "@radix-ui/react-avatar": "^1.0.4",
    "@radix-ui/react-button": "^1.0.3",
    "@radix-ui/react-card": "^1.0.4",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-form": "^0.0.3",
    "@radix-ui/react-input": "^1.0.4",
    "@radix-ui/react-label": "^2.0.2",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-separator": "^1.0.3",
    "@radix-ui/react-slot": "^1.0.2",
    "@radix-ui/react-table": "^1.0.4",
    "@radix-ui/react-tabs": "^1.0.4",
    "@radix-ui/react-toast": "^1.1.5",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "lucide-react": "^0.279.0",
    "sonner": "^1.2.4",
    "tailwind-merge": "^1.14.0",
    "tailwindcss-animate": "^1.0.7"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "@vitejs/plugin-react": "^4.0.3",
    "autoprefixer": "^10.4.14",
    "eslint": "^8.45.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.3",
    "postcss": "^8.4.27",
    "tailwindcss": "^3.3.3",
    "typescript": "^5.0.2",
    "vite": "^4.4.5"
  }
}
EOF

# 4. Docker 설정
echo "🐳 Docker 설정을 생성합니다..."
cat > docker/docker-compose.yml << 'EOF'
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name:first_ent_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: qpflxktm(*)!#%
      MYSQL_DATABASE: first_ent
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    command: --default-authentication-plugin=mysql_native_password

volumes:
  mysql_data:
EOF

# 5. Database 초기화 스크립트
echo "🗄️ Database 초기화 스크립트를 생성합니다..."
cat > database/init.sql << 'EOF'
-- AI 기반 Artist Management Framework Database Schema
-- Database: first_ent

USE first_ent;

-- 1. Artists 테이블 (아티스트 기본 정보)
CREATE TABLE artists (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    real_name VARCHAR(100),
    birth_date DATE,
    gender ENUM('male', 'female', 'other'),
    nationality VARCHAR(50),
    agency VARCHAR(100),
    debut_date DATE,
    status ENUM('active', 'inactive', 'retired') DEFAULT 'active',
    profile_image_url TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Channels 테이블 (채널 정보)
CREATE TABLE channels (
    id INT PRIMARY KEY AUTO_INCREMENT,
    artist_id INT NOT NULL,
    platform ENUM('instagram', 'youtube', 'tiktok', 'twitter') NOT NULL,
    channel_id VARCHAR(100) NOT NULL,
    channel_name VARCHAR(200),
    channel_url TEXT,
    follower_count INT DEFAULT 0,
    following_count INT DEFAULT 0,
    post_count INT DEFAULT 0,
    is_verified BOOLEAN DEFAULT FALSE,
    last_sync_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE,
    UNIQUE KEY unique_channel (artist_id, platform, channel_id)
);

-- 3. Accounts 테이블 (계정 관리)
CREATE TABLE accounts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'manager', 'viewer') DEFAULT 'viewer',
    is_active BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 4. Boards 테이블 (게시판)
CREATE TABLE boards (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    author_id INT NOT NULL,
    board_type ENUM('notice', 'announcement', 'general') DEFAULT 'general',
    is_published BOOLEAN DEFAULT FALSE,
    view_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES accounts(id) ON DELETE CASCADE
);

-- 5. API_Keys 테이블 (API 키 관리)
CREATE TABLE api_keys (
    id INT PRIMARY KEY AUTO_INCREMENT,
    platform ENUM('instagram', 'youtube', 'tiktok', 'twitter') NOT NULL,
    api_name VARCHAR(100) NOT NULL,
    api_key TEXT NOT NULL,
    api_secret TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    last_used_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 6. Database_Configs 테이블 (DB 연결 정보)
CREATE TABLE database_configs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_name VARCHAR(100) NOT NULL UNIQUE,
    host VARCHAR(100) NOT NULL,
    port INT NOT NULL,
    database_name VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL,
    password_encrypted TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 7. Channel_Stats 테이블 (채널 통계)
CREATE TABLE channel_stats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    channel_id INT NOT NULL,
    stat_date DATE NOT NULL,
    follower_count INT DEFAULT 0,
    following_count INT DEFAULT 0,
    post_count INT DEFAULT 0,
    engagement_rate DECIMAL(5,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE,
    UNIQUE KEY unique_channel_date (channel_id, stat_date)
);

-- 8. Posts 테이블 (게시물 정보)
CREATE TABLE posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    channel_id INT NOT NULL,
    post_id VARCHAR(100) NOT NULL,
    post_url TEXT,
    caption TEXT,
    media_type ENUM('image', 'video', 'carousel') NOT NULL,
    media_urls JSON,
    like_count INT DEFAULT 0,
    comment_count INT DEFAULT 0,
    share_count INT DEFAULT 0,
    posted_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE,
    UNIQUE KEY unique_post (channel_id, post_id)
);

-- 인덱스 생성
CREATE INDEX idx_artists_status ON artists(status);
CREATE INDEX idx_channels_platform ON channels(platform);
CREATE INDEX idx_channels_artist ON channels(artist_id);
CREATE INDEX idx_boards_type ON boards(board_type);
CREATE INDEX idx_boards_author ON boards(author_id);
CREATE INDEX idx_channel_stats_date ON channel_stats(stat_date);
CREATE INDEX idx_posts_channel ON posts(channel_id);
CREATE INDEX idx_posts_posted_at ON posts(posted_at);

-- 초기 데이터 삽입
INSERT INTO accounts (username, email, password_hash, role) VALUES 
('admin', 'admin@firstent.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J7v5Q5K2', 'admin');

INSERT INTO artists (name, real_name, nationality, agency, status) VALUES 
('Sample Artist', '홍길동', 'Korea', 'theProjectCompany', 'active');

INSERT INTO channels (artist_id, platform, channel_id, channel_name, follower_count) VALUES 
(1, 'instagram', 'sample_artist_ig', 'Sample Artist Instagram', 10000),
(1, 'youtube', 'UCsample123', 'Sample Artist YouTube', 5002);
EOF

# 6. Backend 기본 파일들 생성
echo "🔧 Backend 기본 파일들을 생성합니다..."

# Flask 앱 설정
cat > backend/app/__init__.py << 'EOF'
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # 설정
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 
        'mysql+pymysql://root:qpflxktm(*)!#%@localhost:3306/first_ent'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 확장 초기화
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # 라우트 등록
    from .routes import artists, channels, accounts, boards, api_keys
    app.register_blueprint(artists.bp, url_prefix='/api/artists')
    app.register_blueprint(channels.bp, url_prefix='/api/channels')
    app.register_blueprint(accounts.bp, url_prefix='/api/accounts')
    app.register_blueprint(boards.bp, url_prefix='/api/boards')
    app.register_blueprint(api_keys.bp, url_prefix='/api/api-keys')
    
    return app
EOF

# 환경 변수 파일
cat > backend/.env << 'EOF'
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://first_ent_user:first_ent_password@localhost:3306/first_ent
FLASK_ENV=development
FLASK_DEBUG=True
EOF

# 7. Frontend 기본 설정
echo "🎨 Frontend 기본 설정을 생성합니다..."

# Vite 설정
cat > frontend/vite.config.ts << 'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
EOF

# TypeScript 설정
cat > frontend/tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
EOF

# TailwindCSS 설정
cat > frontend/tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: 0 },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: 0 },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
EOF

# 8. 실행 스크립트 생성
echo "📜 실행 스크립트들을 생성합니다..."

cat > scripts/start_backend.sh << 'EOF'
#!/bin/bash
cd /Users/veritas-macbookpro/Documents/work/first_ent/backend
source venv/bin/activate
export FLASK_APP=app
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5002
EOF

cat > scripts/start_frontend.sh << 'EOF'
#!/bin/bash
cd /Users/veritas-macbookpro/Documents/work/first_ent/frontend
npm run dev
EOF

cat > scripts/start_docker.sh << 'EOF'
#!/bin/bash
cd /Users/veritas-macbookpro/Documents/work/first_ent/docker
docker-compose up -d
EOF

# 실행 권한 부여
chmod +x scripts/*.sh

# Backend 환경 설정 함수
setup_backend_environment() {
  echo "🐍 Backend 환경을 설정합니다..."
  cd "$PROJECT_ROOT/backend"

  if [ ! -d ".venv" ]; then
    echo "  - 가상 환경(.venv)이 존재하지 않습니다. 새로 생성합니다."
    python3 -m venv .venv
  else
    echo "  - 기존 가상 환경(.venv)을 사용합니다."
  fi

  echo "  - 가상 환경을 활성화합니다."
  source .venv/bin/activate

  echo "  - requirements.txt 파일로부터 패키지를 설치합니다."
  pip install -r requirements.txt

  echo "  - Backend 환경 설정이 완료되었습니다."
  deactivate
}

# 9. README 업데이트
echo "📝 README를 업데이트합니다..."
cat >> README.md << 'EOF'

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
3. 계정 관리 시스템
4. 게시판 관리
5. API 키 관리
6. 데이터베이스 설정 관리
EOF

echo "✅ 프로젝트 초기화가 완료되었습니다!"
echo ""
echo "다음 단계를 따라 프로젝트를 실행하세요:"
echo "1. Docker 컨테이너 시작: ./scripts/start_docker.sh"
setup_backend_environment
echo "2. Backend 설정: cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
echo "3. Frontend 설정: cd frontend && npm install"
echo "4. Backend 실행: ./scripts/start_backend.sh"
echo "5. Frontend 실행: ./scripts/start_frontend.sh"
