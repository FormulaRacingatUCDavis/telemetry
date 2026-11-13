#!/bin/bash
set -e

cd ../dashboard

# building dashboard
docker build -t driver-dashboard .

# creating network for to connect to mosquitto
TELEMTRY_NETWORK_NAME="raspi-telemhost-firmware_default"

# enable dashboard to display
xhost +local:docker

# runs dashboard
docker run --rm -dt \
  --network ${TELEMTRY_NETWORK_NAME} \
  -e DISPLAY=$DISPLAY \
  -e QT_QPA_PLATFORM=xcb \
  -e QT_QUICK_BACKEND=software \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v "$HOME/.Xauthority:/root/.Xauthority:rw" \
  --name driver-dashboard \
  driver-dashboard

echo "dashboard ready"
