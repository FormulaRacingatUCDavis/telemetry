#!/bin/bash

cd ../dashboard

# removing container if exists
docker rm -f driver-dashboard vcan-network 2>/dev/null || true
# building dashboard
docker build -t driver-dashboard .

# creating network for to connect to mosquitto
TELEMTRY_NETWORK_NAME="raspi-telemhost-firmware_default"

# enable dashboard to display
xhost +local:docker

# creates container with vcan connected to defualt network so still has access to mosquitto
# only use when testing with vcan
docker rm -f vcan-network 2>/dev/null || true
docker run -d --name vcan-network \
  --network raspi-telemhost-firmware_default \
  --cap-add=NET_ADMIN \
  alpine sh -c "apk add --no-cache iproute2 && ip link add dev vcan0 type vcan && ip link set up vcan0 && tail -f /dev/null"

# wait until vcan setup
until docker exec vcan-network ip link show vcan0 >/dev/null 2>&1; do sleep 0.5; done
echo "vcan set up"

# use only for testing with vcan else use docker run below
docker run --rm -dt \
  --network container:vcan-network \
  -e DISPLAY=$DISPLAY \
  -e QT_QPA_PLATFORM=xcb \
  -e QT_QUICK_BACKEND=software \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v "$HOME/.Xauthority:/root/.Xauthority:rw" \
  --name driver-dashboard \
  driver-dashboard

# runs dashboard
# docker run --rm -dt \
#   --network ${TELEMTRY_NETWORK_NAME} \
#   --network vcan-network \
#   -e DISPLAY=$DISPLAY \
#   -e QT_QPA_PLATFORM=xcb \
#   -e QT_QUICK_BACKEND=software \
#   -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
#   -v "$HOME/.Xauthority:/root/.Xauthority:rw" \
#   --name driver-dashboard \
#   driver-dashboard

echo "dashboard ready"
