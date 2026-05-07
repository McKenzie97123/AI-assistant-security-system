#!/usr/bin/env bash
set -euo pipefail

REGISTRY=${REGISTRY:-"aisys"}
TAG=${TAG:-"latest"}

echo "==> Building Docker images (registry=$REGISTRY tag=$TAG)"

docker build -t "$REGISTRY/webapp:$TAG"     src/webapp
docker build -t "$REGISTRY/protection:$TAG" src/protection
docker build -t "$REGISTRY/bots:$TAG"       src/bots

echo "==> Done."
