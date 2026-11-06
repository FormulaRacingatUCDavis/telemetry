#!/bin/bash

cd ../dashboard

# building dashboard
docker build -t driver-dashboard .

# creating network for to connect to mosquitto
NETWORK_NAME="mqtt-network"
if [ -z "$(docker network ls --filter name=^${NETWORK_NAME}$ --format '{{.Name}}')" ]; then
    echo "Creating docker network: ${NETWORK_NAME}"
    docker network create ${NETWORK_NAME}
else 
    echo "network '${NETWORK_NAME}' already exists"
fi

# running network, "mosquitto" is the docker container with mqtt
docker run -d \
    --name mosquitto \
    --network ${NETWORK_NAME} \
    eclipse-mosquitto:2

echo "network is running"

# enable dashboard to display
xhost +local:docker

# runs dashboard
docker run --rm -it \
  --network ${NETWORK_NAME} \
  -e DISPLAY=$DISPLAY \
  -e QT_QPA_PLATFORM=xcb \
  -e QT_QUICK_BACKEND=software \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v "$HOME/.Xauthority:/root/.Xauthority:rw" \
  driver-dashboard

echo "dashboard ready"
