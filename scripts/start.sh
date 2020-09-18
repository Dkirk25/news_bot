#!/bin/bash

cd ..
docker build . -t newsbotapp
docker run newsbotapp:latest