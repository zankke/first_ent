#!/bin/bash

# FirstEnt v2: 통합 프로젝트 시작 최적화 스크립트
# UTF-8 (한글 깨짐 방지)
export LANG=ko_KR.UTF-8
export LC_ALL=ko_KR.UTF-8

# 프로젝트 루트 기준
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT" || exit 1

# 공통: 포트 할당 및 점유 중 프로세스 처리 함수
choose_and_assign_app_port() {
    local DEFAULT_PORT=$1
    local SERVICE_KEYWORD=$2
    local PORT=$DEFAULT_PORT
    for try in 0 1; do
        local PID=$(lsof -t -iTCP:"$PORT" -sTCP:LISTEN 2>/dev/null)
        if [ -z "$PID" ]; then
            echo "   ✅ 포트 $PORT 사용가능." >&2 # Redirect to stderr
            echo "$PORT"; return 0
        fi
        local CMDLINE=$(ps -p "$PID" -o command= 2>/dev/null)
        if [[ "$CMDLINE" == *"$SERVICE_KEYWORD"* ]]; then
            echo "   ⚠️  포트 $PORT 자가 프로세스(PID:$PID) 점유중. 강제 종료 후 재할당." >&2 >&2 # Redirect to stderr
            kill -9 "$PID" 2>/dev/null; sleep 1
            echo "   ✅ 포트 $PORT 재사용." >&2 >&2 # Redirect to stderr
            echo "$PORT"; return 0
        fi
        [ $try -eq 0 ] && PORT=$((DEFAULT_PORT+10)) && [ "$PORT" -le 10000 ] || {
            echo "❌ 포트 $DEFAULT_PORT, $PORT 모두 외부 점유중. 종료."; return 1; } >&2 # Redirect to stderr
    done
}

echo -e "🚀 FirstEnt v2 시작\n📁 ROOT: $PROJECT_ROOT"

# Function to wait for MySQL to be ready
wait_for_db() {
    local DB_HOST=$1
    local DB_PORT=$2
    local DB_USER=$3
    local DB_PASSWORD=$4
    local DB_NAME=$5
    echo "   ⏳ Waiting for DB at $DB_HOST:$DB_PORT/$DB_NAME..."
    for i in {1..30}; do # wait for up to 30 seconds
        if nc -z "$DB_HOST" "$DB_PORT" &>/dev/null; then
            echo "   ✅ DB port is open!"
            return 0
        fi
        sleep 1
    done
    echo "❌ DB did not become ready in time. Exiting."
    exit 1
}

############################################
# 백엔드 로드
############################################
echo -e "\n🔧 백엔드 준비 중..."

cd "$PROJECT_ROOT/backend" || exit 1

# .venv 구성 및 활성화
if [ ! -d ".venv" ]; then
    echo "📦 Python .venv 생성..."
    python3 -m venv .venv || { echo "❌ venv 실패"; exit 1; }
    echo "✅ .venv 생성"
else
    echo "✅ .venv 존재"
fi
echo "🔌 .venv 활성화"; source .venv/bin/activate || { echo "❌ venv 활성화 실패"; exit 1; }

# 의존성 설치
pip install -r requirements.txt || { echo "❌ 패키지 설치 실패"; exit 1; }
echo "✅ Python 패키지 설치"

# DB 구성 및 SSH 터널 (env 파싱)
echo "🗄️  DB 마이그레이션..."

ENV_FILE="$PROJECT_ROOT/backend/.env"
SSH_TUNNEL_PORT=13306; SSH_TUNNEL_PID=""

if [ -f "$ENV_FILE" ]; then
    # env 직접 1회만 파싱
    while IFS='=' read -r k v; do
        [ -z "$v" ] && continue
        v=$(echo "$v" | tr -d '"' | tr -d "'" | xargs)
        case $k in
            DB_USER) DB_USER=$v;;
            DB_PASSWORD) DB_PASSWORD=$v;;
            DB_HOST) DB_HOST=$v;;
            DB_PORT) DB_PORT=$v;;
            DB_NAME) DB_NAME=$v;;
            SSH_HOST) SSH_HOST=$v;;
            SSH_USER) SSH_USER=$v;;
        esac
    done < <(grep -E '^(DB_USER|DB_PASSWORD|DB_HOST|DB_PORT|DB_NAME|SSH_HOST|SSH_USER)=' "$ENV_FILE")

    if [ "$DB_HOST" ] && [ "$DB_PORT" ]; then
        echo "   📋 DB: $DB_USER@$DB_HOST:$DB_PORT/$DB_NAME"
        # SSH 터널 자동 설정 (로컬 X)
        if [[ "$DB_HOST" != "localhost" && "$DB_HOST" != "127.0.0.1" && "$SKIP_SSH_TUNNEL" != "true" ]]; then
            SSH_HOST=${SSH_HOST:-$DB_HOST}
            if [ "$SSH_HOST" ]; then
                SSH_TARGET="${SSH_USER:-root}@${SSH_HOST}"
                echo "   🔗 SSH 터널: $SSH_TARGET"
                EXISTING_TUNNEL=$(lsof -t -i:$SSH_TUNNEL_PORT 2>/dev/null)
                if [ "$EXISTING_TUNNEL" ]; then
                    echo "   ✅ 기존 SSH 터널($SSH_TUNNEL_PORT)"
                    SSH_TUNNEL_PID="$EXISTING_TUNNEL"
                else
                    ssh -f -N -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -L $SSH_TUNNEL_PORT:127.0.0.1:$DB_PORT $SSH_TARGET 2>/dev/null && sleep 1
                    SSH_TUNNEL_PID=$(lsof -t -i:$SSH_TUNNEL_PORT 2>/dev/null | head -1)
                    [ "$SSH_TUNNEL_PID" ] && echo "   ✅ SSH 터널 완료 ($SSH_TUNNEL_PORT → $DB_HOST:$DB_PORT)" || echo "   ⚠️  SSH 터널 확인 실패"
                fi
            fi
        fi
    fi
else
    echo "   ⚠️  backend/.env 파일 없음."
fi

# Check if 'mysql-dev' container is running and use it if so
if docker ps --format '{{.Names}}' | grep -q 'mysql-dev'; then
    echo "   🐳 'mysql-dev' Docker container detected. Overriding DB connection details."
    export DB_HOST="127.0.0.1"
    export DB_PORT="3306"
    # Set DB_USER, DB_PASSWORD, DB_NAME for the 'mysql-dev' container
    export DB_USER="root"
    export DB_PASSWORD="qpflxktm(*)!#%" # Correct password for mysql-dev
    export DB_NAME="first_ent"
    # Set a flag to skip SSH tunnel if connecting to a local Docker container
    SKIP_SSH_TUNNEL="true"
else
    echo "   ⚠️  'mysql-dev' Docker container not found or not running, falling back to .env or default settings."
fi

export PYTHONPATH=$PROJECT_ROOT
export FLASK_APP=backend.app:create_app

# SSH 터널 사용시 DB 환경 재설정
if [ "$SSH_TUNNEL_PID" ] || lsof -t -i:$SSH_TUNNEL_PORT 2>/dev/null >/dev/null; then
    export DB_HOST="127.0.0.1"
    export DB_PORT="$SSH_TUNNEL_PORT"
    echo "   🔄 SSH 터널 연결: 127.0.0.1:$SSH_TUNNEL_PORT"
fi

# Wait for DB to be ready
if [ "$DB_HOST" ] && [ "$DB_PORT" ] && [ "$DB_USER" ] && [ "$DB_PASSWORD" ] && [ "$DB_NAME" ]; then
    wait_for_db "$DB_HOST" "$DB_PORT" "$DB_USER" "$DB_PASSWORD" "$DB_NAME"
else
    echo "   ⚠️  Insufficient DB connection details to wait for DB."
fi

# DB migration 오류 캐치 (계속 진행)
DB_OUTPUT=$(flask db upgrade 2>&1) || DB_ERROR=$?
if [ "$DB_ERROR" ]; then
    # 대표적인 에러만 체크
    if echo "$DB_OUTPUT" | grep -E "(Unknown database|Can't connect|Operation timed out)" &>/dev/null; then
        echo "⚠️  데이터베이스 연결 실패"
        if [ "$DB_HOST" ] && [ "$DB_PORT" ]; then
            echo "   연결 정보: $DB_USER@${DB_HOST}:${DB_PORT}/$DB_NAME"
            [ "$SSH_TUNNEL_PID" ] && echo "   - SSH 터널은 생성되었으나 DB 연결실패." || echo "   - 서버 미연결 또는 DB 없음. SSH 변수를 .env에 추가하세요."
            echo "   - 방화벽/DB 확인 또는 생성."
        fi
    else
        echo "⚠️  DB 마이그레이션 경고 (계속 진행)"
    fi
else
    echo "✅ DB 마이그레이션 완료"
fi

# 백엔드 서버 기동
cd "$PROJECT_ROOT"
BACKEND_PORT=5002 # Hardcode backend port to 5002
cd "$PROJECT_ROOT/backend" # Ensure we are in the backend directory
export FLASK_APP=backend.app:create_app
export FLASK_RUN_SET_AUTORELOAD=0
export FLASK_ENV=development # Or 'production' based on context, but 'development' for now
echo "DEBUG: BACKEND_PORT value: $BACKEND_PORT"
nohup flask run --host=0.0.0.0 --port=$BACKEND_PORT > flask_nohup.log 2>&1 &
SERVER_PID=$!
echo "$SERVER_PID" > "$PROJECT_ROOT/backend/backend.pid" # Assuming backend.pid is in backend dir
echo "Flask server started with nohup. Logs are being written to flask_nohup.log. PID: $SERVER_PID"
cd "$PROJECT_ROOT" # Change back to project root

# 백엔드 포트 정상확인(최대 10초 대기)
for _ in {1..20}; do
    if lsof -nP -iTCP:$BACKEND_PORT -sTCP:LISTEN &>/dev/null; then
        echo "   ✅ 백엔드 준비 ($BACKEND_PORT)";
        break;
    fi
    sleep 0.5;
done

############################################
# Puppeteer 서비스
############################################
echo -e "\n🌐 Puppeteer 서비스 준비..."

cd "$PROJECT_ROOT/puppeteer_service" || exit 1

PUPPETEER_DEFAULT_PORT=3001
PUPPETEER_PORT=$(choose_and_assign_app_port $PUPPETEER_DEFAULT_PORT "node server.js") || { echo "❌ Puppeteer 실행불가. 종료"; exit 1; }
[ -d "node_modules" ] || { echo "📦 Puppeteer npm install..."; npm install || { echo "❌ Puppeteer npm 실패"; exit 1; }; }
echo "🚀 Puppeteer 시작..."
PORT=$PUPPETEER_PORT nohup node server.js > puppeteer_nohup.log 2>&1 &
sleep 5

for _ in {1..20}; do lsof -nP -iTCP:$PUPPETEER_PORT -sTCP:LISTEN &>/dev/null && { echo "   ✅ Puppeteer 준비 ($PUPPETEER_PORT)"; break; } ; sleep 0.5; done

cd "$PROJECT_ROOT"

############################################
# 프론트엔드 단계
############################################
echo -e "\n⚛️  프론트엔드 준비..."

cd "$PROJECT_ROOT/frontend" || exit 1
export PATH="/opt/homebrew/bin:$PATH"
[ -s "$HOME/.nvm/nvm.sh" ] && { source "$HOME/.nvm/nvm.sh"; nvm use 22 2>/dev/null || echo "⚠️  nvm use 22 실패, 기본 Node 사용"; }

[ -d node_modules ] || { echo "📦 npm install..."; npm install || { echo "❌ npm 실패"; exit 1; }; }
echo "🚀 프론트엔드 시작..."

cd "$PROJECT_ROOT"
FRONTEND_PORT=3002 # Hardcode frontend port to 3002
cd "$PROJECT_ROOT/frontend" # Ensure we are in the frontend directory
echo "Starting frontend server on port $FRONTEND_PORT using nohup (detached mode)"
nohup npm run dev -- --port "$FRONTEND_PORT" > "$PROJECT_ROOT/frontend/frontend_nohup.log" 2>&1 &

for _ in {1..40}; do lsof -nP -iTCP:$FRONTEND_PORT -sTCP:LISTEN &>/dev/null && { echo "   ✅ 프론트엔드 준비 ($FRONTEND_PORT)"; break; } ; sleep 0.5; done

############################################
# 서버/로그 상태 출력
############################################
echo -e "\n✨ 서버 시작 완료!\n\n📊 서버 상태:"
BACKEND_PID_FINAL=$(lsof -t -i:$BACKEND_PORT 2>/dev/null | head -1)
FRONTEND_PID_FINAL=$(lsof -t -i:$FRONTEND_PORT 2>/dev/null | head -1)
PUPPETEER_PID_FINAL=$(lsof -t -i:$PUPPETEER_PORT 2>/dev/null | head -1)
[ "$BACKEND_PID_FINAL" ] && echo "   백엔드:   http://0.0.0.0:$BACKEND_PORT (PID: $BACKEND_PID_FINAL) ✅" || echo "   백엔드:   http://0.0.0.0:$BACKEND_PORT ❌"
[ "$FRONTEND_PID_FINAL" ] && echo "   프론트엔드: http://localhost:$FRONTEND_PORT (PID: $FRONTEND_PID_FINAL) ✅" || echo "   프론트엔드: http://localhost:$FRONTEND_PORT ❌"
[ "$PUPPETEER_PID_FINAL" ] && echo "   Puppeteer: http://localhost:$PUPPETEER_PORT (PID: $PUPPETEER_PID_FINAL) ✅" || echo "   Puppeteer: http://localhost:$PUPPETEER_PORT ❌"

echo -e "\n📝 로그 확인:\n   백엔드:   tail -f $PROJECT_ROOT/backend/flask_nohup.log\n   프론트엔드: tail -f $PROJECT_ROOT/frontend/frontend_nohup.log"

echo -e "\n🛑 서버 종료:"
[ "$BACKEND_PID_FINAL" ]   && echo "   백엔드:   kill $BACKEND_PID_FINAL  또는  lsof -t -i:$BACKEND_PORT | xargs kill -9"
[ "$FRONTEND_PID_FINAL" ]  && echo "   프론트엔드: kill $FRONTEND_PID_FINAL  또는  lsof -t -i:$FRONTEND_PORT | xargs kill -9"
[ "$PUPPETEER_PID_FINAL" ] && echo "   Puppeteer: kill $PUPPETEER_PID_FINAL  또는  lsof -t -i:$PUPPETEER_PORT | xargs kill -9"
if [ "$SSH_TUNNEL_PID" ]; then
    echo -e "   SSH 터널: kill $SSH_TUNNEL_PID  또는  lsof -t -i:$SSH_TUNNEL_PORT | xargs kill -9\n"
    echo "💡 SSH 터널 정보:"
    echo "   터널 PID: $SSH_TUNNEL_PID"
    echo "   로컬 포트: $SSH_TUNNEL_PORT -> $DB_HOST:$DB_PORT"
    echo "   SSH 호스트: ${SSH_USER:-root}@${SSH_HOST:-$DB_HOST}"
fi
echo ""

