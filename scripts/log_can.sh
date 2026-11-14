#!/bin/bash

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cleanup() {
    kill "$PID" 2>/dev/null
    wait "$PID" 2>/dev/null
    mv "$REPO_DIR/data/can/intake"/candump-*.log "$REPO_DIR/data/can/staging/" 2>/dev/nullsta
    mosquitto_pub -h localhost -p 1883 -t "can/log/status" -m "{\"status\":\"off\"}" -r
    echo "finished logging"
    
}

trap cleanup EXIT
trap 'exit 0' TERM INT

cd "$REPO_DIR/data/can/intake" || exit 1

# make sure the message published matches the message expected in the dashboard when it subscribes to it
 mosquitto_pub -h localhost -p 1883 -t "can/log/status" -m "{\"status\":\"on\"}" -r 
echo "started logging" 

candump -l vcan0 vcan1 &
PID=$!

wait "$PID"