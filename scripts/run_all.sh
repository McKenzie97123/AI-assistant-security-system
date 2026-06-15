#!/usr/bin/env bash
# Pełny zestaw eksperymentów do pracy dyplomowej.
set -euo pipefail
cd "$(dirname "$0")/.."

rm -f results/results.csv

echo "##### CZĘŚĆ 1: porównanie strategii (3 boty) #####"
./scripts/measure.sh rate_limit 3 90
./scripts/measure.sh rules      3 90
./scripts/measure.sh ml         3 90
./scripts/measure.sh llm        3 150

echo "##### CZĘŚĆ 2: skalowalność ataku (strategia ml) #####"
./scripts/measure.sh ml 1 90
./scripts/measure.sh ml 5 90
./scripts/measure.sh ml 10 90

echo "##### WSZYSTKIE EKSPERYMENTY ZAKOŃCZONE #####"
cat results/results.csv
