#!/bin/bash
set -e

cd ../dashboard

# removing container if exists
docker rm -f driver-dashboard vcan-network 2>/dev/null || true
# building dashboard
docker build -t driver-dashboard .

# creating network for to connect to mosquitto
TELEMTRY_NETWORK_NAME="raspi-telemhost-firmware_default"

# enable dashboard to display
export DISPLAY=:1
xhost +SI:localuser:root

# runs dashboard
docker run --rm -dt \
  --network host \
  -e DISPLAY=$DISPLAY \
  -e QT_QPA_PLATFORM=xcb \
  -e QT_QUICK_BACKEND=software \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v "${XAUTHORITY:-$HOME/.Xauthority}:/root/.Xauthority:rw" \
  --name driver-dashboard \
  driver-dashboard
