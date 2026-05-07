#!/usr/bin/env bash
set -euo pipefail

echo "==> Creating namespaces"
kubectl apply -f k8s/namespaces.yaml

echo "==> Deploying webapp"
kubectl apply -f k8s/webapp/

echo "==> Deploying Redis + Ollama + AI protection"
kubectl apply -f k8s/redis/
kubectl apply -f k8s/ollama/
kubectl apply -f k8s/protection/

echo "==> Deploying spam bots"
kubectl apply -f k8s/bots/

echo "==> Deploying monitoring (Prometheus + Grafana)"
kubectl apply -f k8s/monitoring/

echo ""
echo "==> Waiting for core components..."
kubectl rollout status deployment/webapp        -n aisys-webapp     --timeout=120s
kubectl rollout status deployment/redis         -n aisys-protection --timeout=120s
kubectl rollout status deployment/ai-protection -n aisys-protection --timeout=120s
kubectl rollout status deployment/spam-bots     -n aisys-bots       --timeout=120s

echo ""
echo "==> Uwaga: Ollama pobiera model llama3.2:1b (~600 MB) przy pierwszym starcie."
echo "    Sprawdź postęp: kubectl logs -f deployment/ollama -n aisys-protection"
echo "    Strategia 'llm' bedzie gotowa gdy pojawi sie: 'Model gotowy.'"
echo ""
echo "==> Access points:"
echo "    Proxy:      minikube service ai-protection-svc -n aisys-protection"
echo "    Grafana:    minikube service grafana-svc -n aisys-monitoring"
echo "    Prometheus: minikube service prometheus-svc -n aisys-monitoring"
