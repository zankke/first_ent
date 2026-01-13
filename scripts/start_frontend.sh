#!/bin/bash

# 프로젝트 루트 디렉토리 찾기
SCRIPT_DIR=$(cd "$(dirname "$0")"; pwd)
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.."; pwd)

# 💡 Node.js/Homebrew bin 경로를 PATH에 추가
export PATH="/opt/homebrew/bin:$PATH"

# nvm 로드 및 Node.js 22 사용
if [ -s "$HOME/.nvm/nvm.sh" ]; then
    source "$HOME/.nvm/nvm.sh"
    nvm use 22 2>/dev/null || echo "⚠️  nvm use 22 실패, 현재 Node.js 버전 사용"
elif [ -s "/opt/homebrew/opt/nvm/nvm.sh" ]; then
    source "/opt/homebrew/opt/nvm/nvm.sh"
    nvm use 22 2>/dev/null || echo "⚠️  nvm use 22 실패, 현재 Node.js 버전 사용"
fi

# PID file for the frontend process
PID_FILE="$PROJECT_ROOT/frontend/frontend.pid"

# Function to check if a port is in use
is_port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Function to kill a process listening on a given port
kill_process_on_port() {
    local PORT_TO_KILL=$1
    echo "Attempting to kill process on port $PORT_TO_KILL..."
    PIDS=$(lsof -t -i :$PORT_TO_KILL)
    if [ -n "$PIDS" ]; then
        for PID in $PIDS; do
            echo "Killing process $PID on port $PORT_TO_KILL..."
            kill -9 "$PID" >/dev/null 2>&1
        done
        sleep 1 # Give some time for the port to free up
        if is_port_in_use "$PORT_TO_KILL"; then
            echo "Warning: Process on port $PORT_TO_KILL could not be killed."
            return 1 # Indicate failure
        fi
        echo "Process on port $PORT_TO_KILL killed successfully."
    else
        echo "No process found on port $PORT_TO_KILL."
    fi
    return 0 # Indicate success
}

# Function to find an available port, incrementing by 10 if necessary, and handle PID files
find_and_assign_port() {
    local DEFAULT_PORT=$1
    local PID_FILE=$2
    local CURRENT_PORT=$DEFAULT_PORT
    local MAX_PORT=65535 # Maximum port number

    # Try to clean up previous run if PID file exists
    if [ -f "$PID_FILE" ]; then
        local OLD_PID=$(cat "$PID_FILE")
        if ps -p $OLD_PID >/dev/null && is_port_in_use "$DEFAULT_PORT"; then
            echo "Previous frontend instance (PID $OLD_PID) found on default port $DEFAULT_PORT. Killing it..." >&2
            kill -9 "$OLD_PID" >/dev/null 2>&1
            sleep 1
            if is_port_in_use "$DEFAULT_PORT"; then
                echo "Warning: Previous instance (PID $OLD_PID) could not be killed. Will try another port." >&2
            else
                echo "Previous instance killed successfully. Reusing default port." >&2
                echo $DEFAULT_PORT
                return 0
            fi
        fi
        rm -f "$PID_FILE" # Clean up stale PID file >&2
    fi

    # Loop to find an available port
    while true; do
        if is_port_in_use "$CURRENT_PORT"; then
            echo "Port $CURRENT_PORT is in use by another application. Trying next available port (+10)..." >&2
            # Attempt to kill if it's not our previous PID
            kill_process_on_port "$CURRENT_PORT" >&2
            if is_port_in_use "$CURRENT_PORT"; then # If still in use after attempt to kill
                CURRENT_PORT=$((CURRENT_PORT + 10))
                if [ "$CURRENT_PORT" -gt "$MAX_PORT" ]; then
                    echo "Error: Could not find a free port within range." >&2
                    exit 1
                fi
            else
                echo "Process on port $CURRENT_PORT killed. Reusing this port." >&2
                echo $CURRENT_PORT
                return 0
            fi
        else
            echo "Using port $CURRENT_PORT" >&2
            echo $CURRENT_PORT
            return 0
        fi
    done
}


# ===============================================
# Start Frontend server
# ===============================================

# Use the port passed from the calling script or default to 3002
DEFAULT_FRONTEND_PORT=3002 # Default frontend port
# Let the user override if they explicitly set FRONTEND_CURRENT_PORT
# Otherwise, find an available port starting from DEFAULT_FRONTEND_PORT
if [ -z "$FRONTEND_CURRENT_PORT" ]; then
    PORT=$(find_and_assign_port "$DEFAULT_FRONTEND_PORT" "$PID_FILE" 2>/dev/null)
    if [ $? -ne 0 ]; then
        echo "Exiting due to port assignment failure."
        exit 1
    fi
else
    PORT=$FRONTEND_CURRENT_PORT
    if is_port_in_use "$PORT"; then
        echo "Specified port $PORT is in use. Attempting to kill existing process..."
        kill_process_on_port "$PORT"
        if is_port_in_use "$PORT"; then
            echo "Error: Specified port $PORT is still in use after attempting to kill. Please choose another port or manually resolve."
            exit 1
        fi
    fi
fi

cd "$PROJECT_ROOT/frontend"

# Run the frontend (npm run dev) in nohup (detached) mode
echo "Starting frontend server on port $PORT using nohup (detached mode)"
nohup npm run dev -- --port "$PORT" > "$PROJECT_ROOT/frontend/frontend_nohup.log" 2>&1 &
SERVER_PID=$!
echo "$SERVER_PID" > "$PID_FILE"
disown $SERVER_PID 2>/dev/null || true # Keep disown for frontend
echo "Frontend started with nohup. Logs are being written to frontend_nohup.log. PID: $SERVER_PID"

# Ensure the PID file is cleaned up if the script exits
trap "rm -f \"$PID_FILE\"" EXIT

