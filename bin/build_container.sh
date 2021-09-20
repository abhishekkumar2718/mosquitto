#!/usr/bin/bash

docker run \
  -it \
  --name mosquitto \
  -p 1883:1883 \
  -v $(pwd)/mosquitto:/mosquitto \
  eclipse-mosquitto
