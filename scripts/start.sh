#!/bin/bash
docker build . -t newsbotapp
docker run newsbotapp:latest