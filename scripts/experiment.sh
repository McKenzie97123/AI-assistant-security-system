#!/usr/bin/env bash
# Zmień strategię ochrony i liczbę botów na potrzeby eksperymentu.
# Użycie: ./scripts/experiment.sh <strategia> <repliki_botow>
# Przykład: ./scripts/experiment.sh ml 5
set -euo pipefail

STRATEGY=${1:-"ml"}
BOT_REPLICAS=${2:-3}

echo "==> Experiment: strategy=$STRATEGY bots=$BOT_REPLICAS"

kubectl patch configmap protection-config -n aisys-protection \
  --type merge \
  -p "{\"data\":{\"PROTECTION_STRATEGY\":\"$STRATEGY\"}}"

kubectl rollout restart deployment/ai-protection -n aisys-protection
kubectl rollout status  deployment/ai-protection -n aisys-protection --timeout=60s

kubectl scale deployment/spam-bots -n aisys-bots --replicas="$BOT_REPLICAS"
kubectl rollout status deployment/spam-bots -n aisys-bots --timeout=60s

echo "==> Running. Monitor at Grafana (port-forward or NodePort)."
echo "    kubectl port-forward svc/grafana-svc 3000:3000 -n aisys-monitoring"
