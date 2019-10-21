#!/bin/sh

set -e

DOCKER_IMAGE_VERSION_FILE=VERSION
DOCKER_IMAGE_NAME="prometheus-anomaly-detector"
ARTIFACTORY_URL="https://arti.tw.ee/artifactory/docker-local"

getHttpStatusCodeOfUrl() {
  url=$1
  statusCode="$(curl -o /dev/null --silent --head --write-out '%{http_code}\n' $url)"
  echo $statusCode
}

isDockerImageAlreadyPublishedForVersion() {
  version=$1
  fullPathToVersion="$ARTIFACTORY_URL/$DOCKER_IMAGE_NAME/$version"
  [ $(getHttpStatusCodeOfUrl $fullPathToVersion) -eq 302 ]
}

getVersionFromFile() {
   versionFile=$1
   version=`cat $versionFile`
   echo $version
}

isDockerImageAlreadyPublished() {
  version=$(getVersionFromFile $DOCKER_IMAGE_VERSION_FILE)
  echo "Checking if $DOCKER_IMAGE_NAME:$version is already published ...";
  isDockerImageAlreadyPublishedForVersion $version;
}

execute() {
    if isDockerImageAlreadyPublished;
    then
      echo "Library $DOCKER_IMAGE_NAME:$version is already published";
    else
      echo "Library $DOCKER_IMAGE_NAME:$version is NOT published, publishing...";
      docker login --username "$DEPLOY_REGISTRY_USERNAME" --password "$DEPLOY_REGISTRY_PASSWORD" docker.tw.ee
      cd ./release.sh
    fi
}

execute
