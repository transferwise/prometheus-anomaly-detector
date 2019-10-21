#!/bin/bash

set -e

BASE_REPO_NAME=docker.tw.ee/prometheus-anomaly-detector

version=`cat VERSION`

echo "Version read: $version"

# check if image exist, do not push

./build.sh

docker tag $BASE_REPO_NAME:latest $BASE_REPO_NAME:$version

docker push $BASE_REPO_NAME:latest
docker push $BASE_REPO_NAME:$version

echo "Pushed $BASE_REPO_NAME version: $version"
