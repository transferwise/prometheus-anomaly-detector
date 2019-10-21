#!/bin/bash

set -e

BASE_REPO_NAME=docker.tw.ee/prometheus-anomaly-detector

docker build --pull -t $BASE_REPO_NAME:latest ..

