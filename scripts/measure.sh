#!/usr/bin/env bash
# Uruchamia jeden eksperyment i zbiera metryki do pliku CSV/JSON.
# Użycie: ./scripts/measure.sh <strategia> <repliki_botow> <czas_pomiaru_s>
# Przykład: ./scripts/measure.sh ml 3 120
set -euo pipefail

STRATEGY=${1:-ml}
BOTS=${2:-3}
DURATION=${3:-120}
OUTDIR="results"
mkdir -p "$OUTDIR"

echo "=========================================================="
echo "  Eksperyment: strategia=$STRATEGY  boty=$BOTS  pomiar=${DURATION}s"
echo "=========================================================="

# 1. Ustaw strategię + restart proxy (zeruje liczniki) + skaluj boty
kubectl patch configmap protection-config -n aisys-protection --type merge \
  -p "{\"data\":{\"PROTECTION_STRATEGY\":\"$STRATEGY\"}}" >/dev/null
kubectl rollout restart deployment/ai-protection -n aisys-protection >/dev/null
kubectl rollout status  deployment/ai-protection -n aisys-protection --timeout=90s >/dev/null
kubectl scale deployment/spam-bots -n aisys-bots --replicas="$BOTS" >/dev/null
kubectl rollout status deployment/spam-bots -n aisys-bots --timeout=90s >/dev/null

echo "==> Komponenty gotowe. Generowanie ruchu przez ${DURATION}s..."
sleep "$DURATION"

# 2. Port-forward proxy (dokładne liczniki) i Prometheus (rate/kwantyle)
kubectl port-forward -n aisys-protection svc/ai-protection-svc 18000:8000 >/dev/null 2>&1 &
PF_PROXY=$!
kubectl port-forward -n aisys-monitoring svc/prometheus-svc 19090:9090 >/dev/null 2>&1 &
PF_PROM=$!
trap "kill $PF_PROXY $PF_PROM 2>/dev/null || true" EXIT
sleep 4

METRICS=$(curl -s http://localhost:18000/metrics)

get_counter() { # $1=metric+labels regex ; 0 gdy brak dopasowania
  echo "$METRICS" | { grep -E "^$1" || true; } | awk '{s+=$2} END {printf "%d", s+0}'
}

BLOCKED=$(get_counter 'proxy_requests_total\{result="blocked"\}')
ALLOWED=$(get_counter 'proxy_requests_total\{result="allowed"\}')
TOTAL=$((BLOCKED + ALLOWED))
LAT_SUM=$(echo "$METRICS" | awk '/^proxy_detection_latency_seconds_sum/{print $2; f=1} END{if(!f)print 0}')
LAT_CNT=$(echo "$METRICS" | awk '/^proxy_detection_latency_seconds_count/{print $2; f=1} END{if(!f)print 0}')

prom() { # $1 = promql -> scalar value
  curl -s --data-urlencode "query=$1" http://localhost:19090/api/v1/query \
    | python3 -c "import sys,json
try:
    d=json.load(sys.stdin); r=d['data']['result']; print(r[0]['value'][1] if r else 'NaN')
except Exception:
    print('NaN')"
}

P50=$(prom 'histogram_quantile(0.50, sum(rate(proxy_detection_latency_seconds_bucket[1m])) by (le))')
P95=$(prom 'histogram_quantile(0.95, sum(rate(proxy_detection_latency_seconds_bucket[1m])) by (le))')
P99=$(prom 'histogram_quantile(0.99, sum(rate(proxy_detection_latency_seconds_bucket[1m])) by (le))')
RPS_TOTAL=$(prom 'sum(rate(proxy_requests_total[1m]))')
RPS_BLOCKED=$(prom 'sum(rate(proxy_requests_total{result="blocked"}[1m]))')

BLOCK_RATE=$(python3 -c "print(f'{$BLOCKED/$TOTAL:.4f}' if $TOTAL else '0')")
AVG_LAT_MS=$(python3 -c "print(f'{1000*$LAT_SUM/$LAT_CNT:.3f}' if $LAT_CNT else '0')")

echo ""
echo "------------------- WYNIK -------------------"
printf "strategia      : %s\n" "$STRATEGY"
printf "boty           : %s\n" "$BOTS"
printf "czas pomiaru   : %ss\n" "$DURATION"
printf "zapytania razem: %s\n" "$TOTAL"
printf "zablokowane    : %s\n" "$BLOCKED"
printf "przepuszczone  : %s\n" "$ALLOWED"
printf "block rate     : %s\n" "$BLOCK_RATE"
printf "throughput rps : %s\n" "$RPS_TOTAL"
printf "blocked rps    : %s\n" "$RPS_BLOCKED"
printf "latency avg ms : %s\n" "$AVG_LAT_MS"
printf "latency p50 s  : %s\n" "$P50"
printf "latency p95 s  : %s\n" "$P95"
printf "latency p99 s  : %s\n" "$P99"
echo "---------------------------------------------"

CSV="$OUTDIR/results.csv"
if [ ! -f "$CSV" ]; then
  echo "strategy,bots,duration_s,total,blocked,allowed,block_rate,rps_total,rps_blocked,avg_lat_ms,p50_s,p95_s,p99_s" > "$CSV"
fi
echo "$STRATEGY,$BOTS,$DURATION,$TOTAL,$BLOCKED,$ALLOWED,$BLOCK_RATE,$RPS_TOTAL,$RPS_BLOCKED,$AVG_LAT_MS,$P50,$P95,$P99" >> "$CSV"
echo "==> Dopisano do $CSV"
