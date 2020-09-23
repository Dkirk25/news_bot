#!/bin/bash

docker build . -t newsbotapp
docker run -it -d newsbotapp:latest