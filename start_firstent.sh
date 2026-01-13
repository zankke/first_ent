#!/bin/bash

# FirstEnt v2 프로젝트 통합 시작 스크립트
# 백엔드와 프론트엔드를 모두 시작합니다.

# UTF-8 인코딩 설정 (한글 깨짐 방지)
export LANG=ko_KR.UTF-8
export LC_ALL=ko_KR.UTF-8

# 프로젝트 루트 디렉토리 찾기
PROJECT_ROOT=$(cd "$(dirname "$0")"; pwd)
cd "$PROJECT_ROOT"

# 함수: 포트 충돌 처리 및 할당
# 인자: 기본 포트, 서비스 식별 키워드 (띄어쓰기로 구분)
check_and_assign_port() {
    local DEFAULT_PORT=$1
    shift
    local SERVICE_KEYWORDS=("$@")
    local CURRENT_PORT=$DEFAULT_PORT
    local MAX_PORT=$((DEFAULT_PORT + 100)) # 최대 100개 포트까지 검색
    local PID=""
    local CMDLINE=""
    local IS_SELF_PROCESS=false

    echo "   ⚙️  ${SERVICE_KEYWORDS[0]} 서비스 포트 ${DEFAULT_PORT} 확인 중..."

    while [ "$CURRENT_PORT" -le "$MAX_PORT" ]; do
        PID=$(lsof -t -iTCP:"$CURRENT_PORT" -sTCP:LISTEN 2>/dev/null)

        if [ -z "$PID" ]; then
            # 포트가 사용 가능함
            echo "   ✅ 포트 ${CURRENT_PORT} (으)로 시작합니다."
            echo "$CURRENT_PORT"
            return 0
        else
            # 포트가 사용 중임
            CMDLINE=$(ps -p "$PID" -o command= 2>/dev/null)
            IS_SELF_PROCESS=false

            for KEYWORD in "${SERVICE_KEYWORDS[@]}"; do
                if echo "$CMDLINE" | grep -q -- "$KEYWORD"; then
                    IS_SELF_PROCESS=true
                    break
                fi
            done

            if $IS_SELF_PROCESS; then
                echo "   ⚠️  포트 ${CURRENT_PORT} 가 이미 사용 중입니다. (PID: ${PID}, 자가 프로세스 재시작)"
                kill -9 "$PID" 2>/dev/null
                sleep 1 # 프로세스 종료 대기
                echo "   ✅ 자가 프로세스를 종료하고 포트 ${CURRENT_PORT} (으)로 재시작합니다."
                echo "$CURRENT_PORT"
                return 0
            else
                echo "   ⚠️  포트 ${CURRENT_PORT} 가 이미 사용 중입니다. (PID: ${PID}, 외부 프로세스). 다음 포트를 시도합니다..."
                CURRENT_PORT=$((CURRENT_PORT + 1))
            fi
        fi
    done

    echo "❌ 사용 가능한 포트를 찾을 수 없습니다. (기본 포트 ${DEFAULT_PORT} 부터 ${MAX_PORT} 까지 검색)" >&2
    return 1
}

echo "🚀 FirstEnt v2 프로젝트를 시작합니다..."
echo "📁 프로젝트 루트: $PROJECT_ROOT"

# ===============================================
# 백엔드 설정 및 시작
# ===============================================
echo ""
echo "🔧 백엔드 서버를 설정하고 시작합니다..."

cd "$PROJECT_ROOT/backend"

# 가상환경 확인 및 생성 (.venv 사용)
if [ ! -d ".venv" ]; then
    echo "📦 Python 가상환경(.venv) 을 생성합니다..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ 가상환경 생성 실패"
        exit 1
    fi
    echo "✅ 가상환경 생성 완료"
else
    echo "✅ 기존 .venv 가상환경 발견"
fi

# 가상환경 활성화
echo "🔌 .venv 가상환경을 활성화합니다..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ 가상환경 활성화 실패"
    exit 1
fi
echo "✅ 가상환경 활성화 완료"

# 의존성 설치
echo "📥 Python 패키지를 설치합니다..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 패키지 설치 실패"
    exit 1
fi
echo "✅ 패키지 설치 완료"

# 데이터베이스 마이그레이션
echo "🗄️  데이터베이스 마이그레이션을 실행합니다..."

# backend/.env 파일에서 DB 연결 정보 읽기
ENV_FILE="$PROJECT_ROOT/backend/.env"
SSH_TUNNEL_PORT=13306  # 로컬 SSH 터널 포트
SSH_TUNNEL_PID=""

if [ -f "$ENV_FILE" ]; then
    # .env 파일에서 DB 정보 추출
    DB_USER=$(grep "^DB_USER=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'" | xargs)
    DB_PASSWORD=$(grep "^DB_PASSWORD=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'" | xargs)
    DB_HOST=$(grep "^DB_HOST=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'" | xargs)
    DB_PORT=$(grep "^DB_PORT=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'" | xargs)
    DB_NAME=$(grep "^DB_NAME=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'" | xargs)
    SSH_HOST=$(grep "^SSH_HOST=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'" | xargs)
    SSH_USER=$(grep "^SSH_USER=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'" | xargs)
    
    if [ ! -z "$DB_HOST" ] && [ ! -z "$DB_PORT" ]; then
        echo "   📋 DB 연결 정보: $DB_USER@$DB_HOST:$DB_PORT/$DB_NAME"
        
        # 원격 호스트인 경우 SSH 터널링 시도
        if [ "$DB_HOST" != "localhost" ] && [ "$DB_HOST" != "127.0.0.1" ]; then
            # SSH_HOST가 설정되어 있으면 SSH 터널 사용, 없으면 DB_HOST를 SSH_HOST로 사용
            if [ -z "$SSH_HOST" ]; then
                SSH_HOST="$DB_HOST"
            fi
            
            if [ ! -z "$SSH_HOST" ]; then
                SSH_TARGET="${SSH_USER:-root}@${SSH_HOST}"
                echo "   🔗 SSH 터널 생성 시도: $SSH_TARGET"
                
                # 기존 터널이 있는지 확인
                EXISTING_TUNNEL=$(lsof -t -i:$SSH_TUNNEL_PORT 2>/dev/null)
                if [ ! -z "$EXISTING_TUNNEL" ]; then
                    echo "   ✅ 기존 SSH 터널 발견 (포트 $SSH_TUNNEL_PORT)"
                    SSH_TUNNEL_PID="$EXISTING_TUNNEL"
                else
                    # SSH 터널 생성 (백그라운드, StrictHostKeyChecking=no로 첫 연결 허용)
                    ssh -f -N -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
                        -L $SSH_TUNNEL_PORT:127.0.0.1:$DB_PORT $SSH_TARGET 2>/dev/null
                    if [ $? -eq 0 ]; then
                        sleep 1
                        SSH_TUNNEL_PID=$(lsof -t -i:$SSH_TUNNEL_PORT 2>/dev/null | head -1)
                        if [ ! -z "$SSH_TUNNEL_PID" ]; then
                            echo "   ✅ SSH 터널 생성 완료 (로컬 포트: $SSH_TUNNEL_PORT -> $DB_HOST:$DB_PORT)"
                        else
                            echo "   ⚠️  SSH 터널 생성 후 확인 실패"
                        fi
                    else
                        echo "   ⚠️  SSH 터널 생성 실패 (SSH 키 인증 또는 연결 문제)"
                        echo "      직접 연결을 시도합니다."
                    fi
                fi
            fi
        fi
    fi
else
    echo "   ⚠️  backend/.env 파일을 찾을 수 없습니다."
fi

export PYTHONPATH=$PROJECT_ROOT
export FLASK_APP=backend.app:create_app

# SSH 터널을 사용하는 경우 환경 변수 설정
if [ ! -z "$SSH_TUNNEL_PID" ] || [ ! -z "$(lsof -t -i:$SSH_TUNNEL_PORT 2>/dev/null)" ]; then
    # 환경 변수로 DB 연결 정보 오버라이드 (마이그레이션용)
    export DB_HOST="127.0.0.1"
    export DB_PORT="$SSH_TUNNEL_PORT"
    echo "   🔄 SSH 터널을 통해 연결: 127.0.0.1:$SSH_TUNNEL_PORT"
fi

# 데이터베이스 마이그레이션 실행 (오류 무시하고 계속 진행)
DB_OUTPUT=$(flask db upgrade 2>&1) || DB_ERROR=$?

if [ ! -z "$DB_ERROR" ]; then
    # 데이터베이스 연결 오류는 경고로 처리
    echo "$DB_OUTPUT" | grep -E "(Unknown database|Can't connect|Operation timed out)" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "⚠️  데이터베이스 연결 실패"
        if [ ! -z "$DB_HOST" ] && [ ! -z "$DB_PORT" ]; then
            ORIGINAL_HOST=$(grep "^DB_HOST=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'" | xargs)
            ORIGINAL_PORT=$(grep "^DB_PORT=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'" | xargs)
            echo "   연결 정보: $DB_USER@${ORIGINAL_HOST:-$DB_HOST}:${ORIGINAL_PORT:-$DB_PORT}/$DB_NAME"
            if [ ! -z "$SSH_TUNNEL_PID" ]; then
                echo "   - SSH 터널은 생성되었지만 데이터베이스 연결에 실패했습니다."
            else
                echo "   - 서버에 연결할 수 없거나 데이터베이스가 없을 수 있습니다."
                echo "   - SSH 터널을 사용하려면 backend/.env에 SSH_HOST와 SSH_USER를 설정하세요."
            fi
            echo "   - 방화벽 설정을 확인하거나 데이터베이스를 생성해주세요."
        fi
        echo "   계속 진행합니다..."
    else
        echo "⚠️  데이터베이스 마이그레이션 경고 (계속 진행)"
    fi
else
    echo "✅ 데이터베이스 마이그레이션 완료"
fi

# 백엔드 서버 시작 (start_backend.sh 사용)
echo "🚀 백엔드 서버를 시작합니다..."
cd "$PROJECT_ROOT"

BACKEND_DEFAULT_PORT=5001
BACKEND_PORT=$(check_and_assign_port $BACKEND_DEFAULT_PORT "flask run")
if [ $? -ne 0 ]; then
    echo "❌ 백엔드 서버를 시작할 수 없습니다. 스크립트를 종료합니다."
    exit 1
fi

# 실행 권한 확인 및 부여
if [ ! -x "$PROJECT_ROOT/scripts/start_backend.sh" ]; then
    echo "🔧 start_backend.sh에 실행 권한을 부여합니다..."
    chmod +x "$PROJECT_ROOT/scripts/start_backend.sh"
fi

# 동적으로 결정된 포트를 사용하여 백엔드 시작
BACKEND_CURRENT_PORT=$BACKEND_PORT "$PROJECT_ROOT/scripts/start_backend.sh"
# 백그라운드 프로세스의 PID는 start_backend.sh 내부에서 시작되므로 포트로 확인
sleep 2

# 백엔드 서버 준비 대기
echo "   백엔드 서버 준비 대기 중..."
sleep 3
for i in {1..20}; do
    sleep 0.5
    if lsof -nP -iTCP:$BACKEND_PORT -sTCP:LISTEN > /dev/null 2>&1; then
        echo "   ✅ 백엔드 서버 준비 완료 (포트 $BACKEND_PORT)"
        break
    fi
    if [ $i -eq 20 ]; then
        echo "   ⚠️  백엔드 서버가 아직 준비되지 않았습니다. (포트 $BACKEND_PORT)"
    fi
done

# ===============================================
# Puppeteer 서비스 설정 및 시작
# ===============================================
echo ""
echo "🌐 Puppeteer 서비스 설정 및 시작합니다..."

cd "$PROJECT_ROOT/puppeteer_service"

PUPPETEER_DEFAULT_PORT=3001
PUPPETEER_PORT=$(check_and_assign_port $PUPPETEER_DEFAULT_PORT "node server.js")
if [ $? -ne 0 ]; then
    echo "❌ Puppeteer 서비스를 시작할 수 없습니다. 스크립트를 종료합니다."
    exit 1
fi

# npm install 확인
if [ ! -d "node_modules" ]; then
    echo "📦 Puppeteer 서비스 npm 패키지를 설치합니다..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Puppeteer 서비스 npm 패키지 설치 실패"
        exit 1
    fi
    echo "✅ Puppeteer 서비스 npm 패키지 설치 완료"
else
    echo "✅ Puppeteer 서비스 기존 node_modules 발견"
fi

# Puppeteer 서비스 시작
echo "🚀 Puppeteer 서비스를 시작합니다..."
PORT=$PUPPETEER_PORT nohup node server.js > puppeteer_nohup.log 2>&1 &
# 백그라운드 프로세스의 PID는 스크립트 내부에서 시작되므로 포트로 확인
sleep 2

# Puppeteer 서비스 준비 대기
echo "   Puppeteer 서비스 준비 대기 중..."
sleep 3
for i in {1..20}; do
    sleep 0.5
    if lsof -nP -iTCP:$PUPPETEER_PORT -sTCP:LISTEN > /dev/null 2>&1; then
        echo "   ✅ Puppeteer 서비스 준비 완료 (포트 $PUPPETEER_PORT)"
        break
    fi
    if [ $i -eq 20 ]; then
        echo "   ⚠️  Puppeteer 서비스가 아직 준비되지 않았습니다. (포트 $PUPPETEER_PORT)"
    fi
done

cd "$PROJECT_ROOT" # 다시 프로젝트 루트로 이동

# ===============================================
# 프론트엔드 설정 및 시작
# ===============================================
echo ""
echo "⚛️  프론트엔드 서버를 설정하고 시작합니다..."

cd "$PROJECT_ROOT/frontend"

# Node.js 경로 설정
export PATH="/opt/homebrew/bin:$PATH"

# nvm 사용 (Node.js 22)
if [ -s "$HOME/.nvm/nvm.sh" ]; then
    source "$HOME/.nvm/nvm.sh"
    nvm use 22 2>/dev/null || echo "⚠️  nvm use 22 실패, 현재 Node.js 버전 사용"
fi

# npm install 확인
if [ ! -d "node_modules" ]; then
    echo "📦 npm 패키지를 설치합니다..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ npm 패키지 설치 실패"
        exit 1
    fi
    echo "✅ npm 패키지 설치 완료"
else
    echo "✅ 기존 node_modules 발견"
fi

# 프론트엔드 서버 시작 (start_frontend.sh 사용)
echo "🚀 프론트엔드 서버를 시작합니다..."
cd "$PROJECT_ROOT"

FRONTEND_DEFAULT_PORT=3002
FRONTEND_PORT=$(check_and_assign_port $FRONTEND_DEFAULT_PORT "npm run dev")
if [ $? -ne 0 ]; then
    echo "❌ 프론트엔드 서버를 시작할 수 없습니다. 스크립트를 종료합니다."
    exit 1
fi

# 실행 권한 확인 및 부여
if [ ! -x "$PROJECT_ROOT/scripts/start_frontend.sh" ]; then
    echo "🔧 start_frontend.sh에 실행 권한을 부여합니다..."
    chmod +x "$PROJECT_ROOT/scripts/start_frontend.sh"
fi

# 동적으로 결정된 포트를 사용하여 프론트엔드 시작
FRONTEND_CURRENT_PORT=$FRONTEND_PORT "$PROJECT_ROOT/scripts/start_frontend.sh"
# 백그라운드 프로세스의 PID는 스크립트 내부에서 시작되므로 포트로 확인
sleep 2

# 프론트엔드 서버 준비 대기
echo "   프론트엔드 서버 준비 대기 중..."
sleep 3
for i in {1..40}; do
    sleep 0.5
    if lsof -nP -iTCP:$FRONTEND_PORT -sTCP:LISTEN > /dev/null 2>&1; then
        echo "   ✅ 프론트엔드 서버 준비 완료 (포트 $FRONTEND_PORT)"
        break
    fi
    if [ $i -eq 40 ]; then
        echo "   ⚠️  프론트엔드 서버가 아직 준비되지 않았습니다. (포트 $FRONTEND_PORT)"
    fi
done

# ===============================================
# 시작 완료 메시지
# ===============================================
echo ""
echo "✨ 서버 시작 프로세스 완료!"
echo ""
echo "📊 서버 상태:"
# 백엔드 PID 확인 및 표시
BACKEND_PID_FINAL=$(lsof -t -i:$BACKEND_PORT 2>/dev/null | head -1)
if [ ! -z "$BACKEND_PID_FINAL" ]; then
    echo "   백엔드:   http://0.0.0.0:$BACKEND_PORT (PID: $BACKEND_PID_FINAL) ✅"
else
    echo "   백엔드:   http://0.0.0.0:$BACKEND_PORT ❌ (시작되지 않음)"
fi
# 프론트엔드 PID 확인 및 표시
FRONTEND_PID_FINAL=$(lsof -t -i:$FRONTEND_PORT 2>/dev/null | head -1)
if [ ! -z "$FRONTEND_PID_FINAL" ]; then
    echo "   프론트엔드: http://localhost:$FRONTEND_PORT (PID: $FRONTEND_PID_FINAL) ✅"
else
    echo "   프론트엔드: http://localhost:$FRONTEND_PORT ❌ (시작되지 않음)"
fi
# Puppeteer PID 확인 및 표시
PUPPETEER_PID_FINAL=$(lsof -t -i:$PUPPETEER_PORT 2>/dev/null | head -1)
if [ ! -z "$PUPPETEER_PID_FINAL" ]; then
    echo "   Puppeteer: http://localhost:$PUPPETEER_PORT (PID: $PUPPETEER_PID_FINAL) ✅"
else
    echo "   Puppeteer: http://localhost:$PUPPETEER_PORT ❌ (시작되지 않음)"
fi
echo ""
echo "📝 로그 확인:"
echo "   백엔드:   tail -f $PROJECT_ROOT/backend/flask_nohup.log"
echo "   프론트엔드: tail -f $PROJECT_ROOT/frontend/frontend_nohup.log"
echo ""
echo "🛑 서버 종료:"
if [ ! -z "$BACKEND_PID_FINAL" ]; then
    echo "   백엔드:   kill $BACKEND_PID_FINAL  또는  lsof -t -i:$BACKEND_PORT | xargs kill -9"
fi
if [ ! -z "$FRONTEND_PID_FINAL" ]; then
    echo "   프론트엔드: kill $FRONTEND_PID_FINAL  또는  lsof -t -i:$FRONTEND_PORT | xargs kill -9"
fi
if [ ! -z "$PUPPETEER_PID_FINAL" ]; then
    echo "   Puppeteer: kill $PUPPETEER_PID_FINAL  또는  lsof -t -i:$PUPPETEER_PORT | xargs kill -9"
fi
if [ ! -z "$SSH_TUNNEL_PID" ]; then
    echo "   SSH 터널: kill $SSH_TUNNEL_PID  또는  lsof -t -i:$SSH_TUNNEL_PORT | xargs kill -9"
    echo ""
    echo "💡 SSH 터널 정보:"
    echo "   터널 PID: $SSH_TUNNEL_PID"
    echo "   로컬 포트: $SSH_TUNNEL_PORT -> $DB_HOST:$DB_PORT"
    echo "   SSH 호스트: ${SSH_USER:-root}@${SSH_HOST:-$DB_HOST}"
fi
echo ""

