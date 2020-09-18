#!/bin/bash

docker build . -t newsbotapp
docker run -d newsbotapp:latestdock