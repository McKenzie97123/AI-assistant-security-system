#!/usr/bin/env python3
"""Renderuje tabele pracy jako grafiki -> results/table_*.png"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")

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
            cell.set_height(cell.get_height() * 1.15)
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
render(
    "table_5_1.png",
    ["Strategia", "Zapytania", "Zablokowane", "Wskaźnik\nblokowania", "Przepustowość\n[żądań/s]", "Średnie\nopóźnienie [ms]"],
    [
        ["Ograniczanie liczby zapytań", "1795", "1435", "79,9%", "19,4", "2,14"],
        ["Detekcja heurystyczna", "1699", "1609", "94,7%", "18,4", "2,04"],
        ["Uczenie maszynowe", "1716", "1482", "86,4%", "18,7", "4,74"],
        ["Model językowy (LLM)", "228", "0", "0,0%", "1,62", "15006,83"],
    ],
    "Tabela 5.1  Porównanie strategii ochrony przy stałej liczbie trzech replik botów",
    col_widths=[0.26, 0.13, 0.14, 0.15, 0.16, 0.16],
)

# Tabela 5.2 — skalowalność (ml)
render(
    "table_5_2.png",
    ["Repliki botów", "Zapytania", "Wskaźnik\nblokowania", "Przepustowość\n[żądań/s]", "Średnie\nopóźnienie [ms]"],
    [
        ["1", "948", "82,9%", "6,3", "3,81"],
        ["3", "1716", "86,4%", "18,7", "4,74"],
        ["5", "2952", "81,5%", "29,7", "5,81"],
        ["10", "5665", "89,7%", "62,3", "4,54"],
    ],
    "Tabela 5.2  Skalowalność ataku dla strategii uczenia maszynowego",
    col_widths=[0.2, 0.2, 0.2, 0.2, 0.2],
)
