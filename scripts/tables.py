#!/usr/bin/env python3
"""Renderuje tabele pracy jako grafiki -> results/table_*.png"""
import csv
import os
import statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")

runs = {}
with open(os.path.join(OUT, "runs_raw.csv")) as fh:
    for r in csv.DictReader(fh):
        runs.setdefault((r["strategy"], int(r["bots"])), []).append(r)


def pm(strategy, bots, col, decimals, scale=1.0):
    """Średnia ± odchylenie standardowe z próby, z przecinkiem dziesiętnym."""
    x = [float(r[col]) * scale for r in runs[(strategy, bots)]]
    return f"{statistics.mean(x):.{decimals}f} ± {statistics.stdev(x):.{decimals}f}".replace(".", ",")

HEADER = "#2c3e50"
ROW_A = "#f4f6f7"
ROW_B = "#ffffff"
EDGE = "#bdc3c7"


def render(filename, columns, rows, title, col_widths=None):
    n_rows = len(rows) + 1
    fig_h = 0.6 + 0.45 * n_rows
    fig_w = 11
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.axis("off")
    table = ax.table(cellText=rows, colLabels=columns, cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.6)

    if col_widths:
        for (r, c), cell in table.get_celld().items():
            cell.set_width(col_widths[c])

    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor(EDGE)
        cell.set_linewidth(0.8)
        if r == 0:
            cell.set_facecolor(HEADER)
            cell.set_text_props(color="white", fontweight="bold")
            cell.set_height(cell.get_height() * 1.6)
        else:
            cell.set_facecolor(ROW_A if r % 2 else ROW_B)

    ax.set_title(title, fontsize=12, fontweight="bold", pad=14)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, filename), dpi=150, bbox_inches="tight")
    plt.close()
    print("Zapisano", filename)


# Tabela 3.1 — rozmieszczenie komponentów
render(
    "table_3_1.png",
    ["Przestrzeń nazw", "Komponent", "Technologia", "Funkcja"],
    [
        ["aisys-webapp", "webapp", "Flask", "Aplikacja-cel z formularzami"],
        ["aisys-protection", "ai-protection", "FastAPI", "Warstwa ochronna (proxy AI)"],
        ["aisys-protection", "redis", "Redis 7", "Magazyn liczników okna czasowego"],
        ["aisys-protection", "ollama", "Ollama (llama3.2:1b)", "Lokalny model LLM"],
        ["aisys-bots", "spam-bots", "Python / requests", "Generator ruchu (boty)"],
        ["aisys-monitoring", "prometheus", "Prometheus", "Zbieranie metryk"],
        ["aisys-monitoring", "grafana", "Grafana", "Wizualizacja metryk"],
    ],
    "Tabela 3.1  Rozmieszczenie komponentów systemu w klastrze Kubernetes",
    col_widths=[0.2, 0.17, 0.22, 0.41],
)

# Tabela 5.1 — porównanie strategii (3 boty)
STRATEGIES = [
    ("rate_limit", "Ograniczanie liczby zapytań", 1, 2),
    ("rules", "Detekcja heurystyczna", 1, 2),
    ("ml", "Uczenie maszynowe", 1, 2),
    ("llm", "Model językowy (LLM)", 2, 1),
]
render(
    "table_5_1.png",
    ["Strategia", "Zapytania", "Zablokowane", "Wskaźnik\nblokowania [%]", "Przepustowość\n[żądań/s]", "Średnie\nopóźnienie [ms]"],
    [
        [name, pm(s, 3, "total", 0), pm(s, 3, "blocked", 0), pm(s, 3, "block_rate", 1, 100),
         pm(s, 3, "rps_total", thr_dec), pm(s, 3, "avg_lat_ms", lat_dec)]
        for s, name, thr_dec, lat_dec in STRATEGIES
    ],
    "Tabela 5.1  Porównanie strategii ochrony przy stałej liczbie trzech replik botów\n(średnia ± odchylenie standardowe, n = 3)",
    col_widths=[0.24, 0.13, 0.13, 0.16, 0.16, 0.18],
)

# Tabela 5.2 — skalowalność (ml)
render(
    "table_5_2.png",
    ["Repliki botów", "Zapytania", "Wskaźnik\nblokowania [%]", "Przepustowość\n[żądań/s]", "Średnie\nopóźnienie [ms]"],
    [
        [str(b), pm("ml", b, "total", 0), pm("ml", b, "block_rate", 1, 100),
         pm("ml", b, "rps_total", 1), pm("ml", b, "avg_lat_ms", 2)]
        for b in (1, 3, 5, 10)
    ],
    "Tabela 5.2  Skalowalność ataku dla strategii uczenia maszynowego\n(średnia ± odchylenie standardowe, n = 3)",
    col_widths=[0.2, 0.2, 0.2, 0.2, 0.2],
)
