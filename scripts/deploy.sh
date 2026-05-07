#!/usr/bin/env bash
set -euo pipefail

echo "==> Creating namespaces"
kubectl apply -f k8s/namespaces.yaml

echo "==> Deploying webapp"
kubectl apply -f k8s/webapp/

echo "==> Deploying Redis + AI protection"
kubectl apply -f k8s/redis/
kubectl apply -f k8s/protection/

echo "==> Deploying spam bots"
kubectl apply -f k8s/bots/

echo "==> Deploying monitoring (Prometheus + Grafana)"
kubectl apply -f k8s/monitoring/

echo ""
echo "==> Done. Waiting for pods..."
kubectl rollout status deployment/webapp        -n aisys-webapp     --timeout=120s
kubectl rollout status deployment/redis         -n aisys-protection --timeout=120s
kubectl rollout status deployment/ai-protection -n aisys-protection --timeout=120s
kubectl rollout status deployment/spam-bots     -n aisys-bots       --timeout=120s

echo ""
echo "==> Access points:"
echo "    Proxy (NodePort): kubectl get svc ai-protection-svc -n aisys-protection"
echo "    Grafana (NodePort): kubectl get svc grafana-svc -n aisys-monitoring"
echo "    Prometheus (NodePort): kubectl get svc prometheus-svc -n aisys-monitoring"
