#!/usr/bin/env python3
"""Generuje wykresy do pracy dyplomowej na podstawie results/results.csv."""
import csv
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(HERE, "results", "results.csv")
OUT = os.path.join(HERE, "results")

STRAT_PL = {
    "rate_limit": "Ograniczanie\nliczby zapytań",
    "rules": "Detekcja\nheurystyczna",
    "ml": "Uczenie\nmaszynowe",
    "llm": "Model\njęzykowy (LLM)",
}

rows = []
with open(CSV) as f:
    for r in csv.DictReader(f):
        rows.append(r)

def f(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return 0.0

# Seria 1: porównanie strategii przy 3 botach
comp = [r for r in rows if int(r["bots"]) == 3]
comp_order = ["rate_limit", "rules", "ml", "llm"]
comp = sorted(comp, key=lambda r: comp_order.index(r["strategy"]) if r["strategy"] in comp_order else 99)

# --- Wykres 1: wskaźnik blokowania wg strategii ---
labels = [STRAT_PL.get(r["strategy"], r["strategy"]) for r in comp]
block = [f(r["block_rate"]) * 100 for r in comp]
plt.figure(figsize=(8, 5))
bars = plt.bar(labels, block, color=["#7f8c8d", "#2980b9", "#27ae60", "#8e44ad"])
plt.ylabel("Wskaźnik blokowania [%]")
plt.title("Skuteczność detekcji botów wg strategii ochrony (3 boty)")
plt.ylim(0, 105)
for b, v in zip(bars, block):
    plt.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.1f}%", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig1_block_rate.png"), dpi=150)
plt.close()

# --- Wykres 2: opóźnienie detekcji (skala log) wg strategii ---
lat = [f(r["avg_lat_ms"]) for r in comp]
plt.figure(figsize=(8, 5))
bars = plt.bar(labels, lat, color=["#7f8c8d", "#2980b9", "#27ae60", "#8e44ad"])
plt.ylabel("Średnie opóźnienie detekcji [ms] (skala log.)")
plt.title("Opóźnienie detekcji wg strategii ochrony (3 boty)")
plt.yscale("log")
for b, v in zip(bars, lat):
    plt.text(b.get_x() + b.get_width() / 2, v * 1.1, f"{v:.2f} ms", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig2_latency.png"), dpi=150)
plt.close()

# --- Wykres 3: przepustowość wg strategii ---
thr = [f(r["rps_total"]) for r in comp]
plt.figure(figsize=(8, 5))
bars = plt.bar(labels, thr, color=["#7f8c8d", "#2980b9", "#27ae60", "#8e44ad"])
plt.ylabel("Przepustowość [żądań/s]")
plt.title("Przepustowość warstwy ochronnej wg strategii (3 boty)")
for b, v in zip(bars, thr):
    plt.text(b.get_x() + b.get_width() / 2, v + 0.3, f"{v:.1f}", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig3_throughput.png"), dpi=150)
plt.close()

# Seria 2: skalowalność (ml) wg liczby botów
scal = sorted([r for r in rows if r["strategy"] == "ml"], key=lambda r: int(r["bots"]))
bots = [int(r["bots"]) for r in scal]
s_block = [f(r["block_rate"]) * 100 for r in scal]
s_thr = [f(r["rps_total"]) for r in scal]
s_lat = [f(r["avg_lat_ms"]) for r in scal]

# --- Wykres 4: skalowalność — blokowanie i przepustowość vs liczba botów ---
fig, ax1 = plt.subplots(figsize=(8, 5))
ax1.set_xlabel("Liczba replik botów")
ax1.set_ylabel("Wskaźnik blokowania [%]", color="#27ae60")
ax1.plot(bots, s_block, "o-", color="#27ae60", linewidth=2, markersize=8, label="Wskaźnik blokowania")
ax1.set_ylim(0, 105)
ax1.tick_params(axis="y", labelcolor="#27ae60")
ax2 = ax1.twinx()
ax2.set_ylabel("Przepustowość [żądań/s]", color="#c0392b")
ax2.plot(bots, s_thr, "s--", color="#c0392b", linewidth=2, markersize=8, label="Przepustowość")
ax2.tick_params(axis="y", labelcolor="#c0392b")
plt.title("Skalowalność ataku — strategia uczenia maszynowego (ml)")
fig.tight_layout()
plt.savefig(os.path.join(OUT, "fig4_scalability.png"), dpi=150)
plt.close()

# --- Wykres 5: skalowalność — opóźnienie vs liczba botów ---
plt.figure(figsize=(8, 5))
plt.plot(bots, s_lat, "o-", color="#2980b9", linewidth=2, markersize=8)
plt.xlabel("Liczba replik botów")
plt.ylabel("Średnie opóźnienie detekcji [ms]")
plt.title("Opóźnienie detekcji w funkcji intensywności ataku (ml)")
for x, y in zip(bots, s_lat):
    plt.text(x, y, f" {y:.2f} ms", va="bottom")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig5_scalability_latency.png"), dpi=150)
plt.close()

print("Zapisano wykresy do", OUT)
for fn in sorted(os.listdir(OUT)):
    if fn.endswith(".png"):
        print(" -", fn)
