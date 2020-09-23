#!/bin/bash

docker build . -t newsbotapp
docker run -it -d dkirk25/newsbotapp:latest