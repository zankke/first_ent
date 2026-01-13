#!/bin/bash

# Navigate to the project root directory
PROJECT_ROOT=$(cd "$(dirname "$0")/.."; pwd)

# Check current Python environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "No virtual environment currently active. Activating project's virtual environment..."
    source "$PROJECT_ROOT/backend/.venv/bin/activate"
else
    echo "A Python virtual environment is already active: $VIRTUAL_ENV"
fi

# Set PYTHONPATH to the project root
export PYTHONPATH=$PROJECT_ROOT

# Flask environment variables
export FLASK_APP=backend.app:create_app
export FLASK_ENV=development
export FLASK_DEBUG=1

# Move to the backend directory
cd "$PROJECT_ROOT/backend"

# Function to hide sensitive information
hide_sensitive_info() {
    sed -E 's:(//[^:@]+):\/\/[HIDDEN]@127.0.0.1:'
}

# PID file for the backend process
PID_FILE="$PROJECT_ROOT/backend/backend.pid"

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
            echo "Previous backend instance (PID $OLD_PID) found on default port $DEFAULT_PORT. Killing it..." >&2
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
        rm -f "$PID_FILE" >&2 # Clean up stale PID file
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
# Start Flask server
# ===============================================

# Use the port passed from the calling script or default to 5001
DEFAULT_BACKEND_PORT=5002 # Set default backend port to 5002 to avoid historical conflicts
# Let the user override if they explicitly set BACKEND_CURRENT_PORT
# Otherwise, find an available port starting from DEFAULT_BACKEND_PORT
if [ -z "$BACKEND_CURRENT_PORT" ]; then
    PORT=$(find_and_assign_port "$DEFAULT_BACKEND_PORT" "$PID_FILE")
    if [ $? -ne 0 ]; then
        echo "Exiting due to port assignment failure."
        exit 1
    fi
else
    PORT=$BACKEND_CURRENT_PORT
    if is_port_in_use "$PORT"; then
        echo "Specified port $PORT is in use. Attempting to kill existing process..."
        kill_process_on_port "$PORT"
        if is_port_in_use "$PORT"; then
            echo "Error: Specified port $PORT is still in use after attempting to kill. Please choose another port or manually resolve."
            exit 1
        fi
    fi
fi

HOST_IP="0.0.0.0"

echo "Starting Flask server on http://$HOST_IP:$PORT using nohup (detached mode)"
nohup flask run --host=$HOST_IP --port=$PORT > flask_nohup.log 2>&1 &
SERVER_PID=$!
echo "$SERVER_PID" > "$PID_FILE"
echo "Flask server started with nohup. Logs are being written to flask_nohup.log. PID: $SERVER_PID"

# Ensure the PID file is cleaned up if the script exits
trap "rm -f \"$PID_FILE\"" EXIT