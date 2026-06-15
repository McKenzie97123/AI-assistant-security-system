#!/usr/bin/env python3
"""Rysuje schemat architektury środowiska badawczego -> results/fig_architecture.png"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis("off")

NS = {  # przestrzenie nazw (tło)
    "bots":    (0.3, 2.6, 2.6, 2.6, "#fdecea", "#e74c3c", "aisys-bots"),
    "prot":    (3.4, 0.4, 5.2, 6.8, "#eaf2fb", "#2980b9", "aisys-protection"),
    "webapp":  (9.1, 4.7, 2.6, 2.0, "#eafaf1", "#27ae60", "aisys-webapp"),
    "mon":     (9.1, 0.4, 2.6, 3.6, "#fef9e7", "#f39c12", "aisys-monitoring"),
}
for x, y, w, h, fc, ec, label in NS.values():
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=fc, ec=ec, lw=1.5, linestyle="--"))
    ax.text(x + 0.12, y + h - 0.28, label, fontsize=10, color=ec, style="italic", fontweight="bold")

def box(x, y, w, h, text, fc="#ffffff", ec="#34495e"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=1.8))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9.5, fontweight="bold")

def arrow(x1, y1, x2, y2, text="", color="#2c3e50", style="-|>", off=0.18):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=16,
                                 lw=1.8, color=color, shrinkA=2, shrinkB=2))
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + off, text, ha="center", fontsize=8.5,
                color=color, fontweight="bold")

# Komponenty
box(0.55, 3.4, 2.1, 1.1, "spam-bots\n(repliki ×N)\nPython/requests", fc="#fdecea", ec="#e74c3c")
box(3.7, 4.7, 2.3, 1.4, "ai-protection\n(proxy AI)\nFastAPI", fc="#d6eaf8", ec="#2980b9")
box(3.7, 2.6, 2.0, 1.0, "Redis\nokno czasowe", fc="#ffffff")
box(6.3, 2.6, 2.0, 1.0, "Ollama\nllama3.2:1b", fc="#ffffff")
box(9.3, 5.3, 2.2, 1.1, "webapp\nFlask\nCSRF + CAPTCHA", fc="#d5f5e3", ec="#27ae60")
box(9.3, 2.5, 2.2, 1.0, "Prometheus", fc="#fcf3cf", ec="#f39c12")
box(9.3, 1.0, 2.2, 1.0, "Grafana", fc="#fcf3cf", ec="#f39c12")

# Decyzja
ax.text(6.05, 6.5, "decyzja:\nBOT / CZŁOWIEK", ha="center", fontsize=8.5,
        color="#8e44ad", fontweight="bold")

# Przepływ
arrow(2.65, 4.0, 3.7, 5.2, "żądanie HTTP", color="#e74c3c", off=0.22)
arrow(6.0, 5.2, 9.3, 5.85, "przepuszczone", color="#27ae60", off=0.22)
arrow(4.85, 4.7, 4.7, 3.6, "RPM/IP", color="#7f8c8d", style="<|-|>", off=0.0)
arrow(5.6, 4.7, 6.9, 3.6, "strategia llm", color="#7f8c8d", style="<|-|>", off=0.0)
arrow(7.2, 5.4, 9.3, 3.5, "scrape /metrics", color="#f39c12", off=0.25)
arrow(10.4, 2.5, 10.4, 2.0, "", color="#f39c12")
# blokada 429
ax.annotate("zablokowane\n(HTTP 429)", xy=(3.85, 4.6), xytext=(2.0, 5.6),
            ha="center", fontsize=8.5, color="#c0392b", fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color="#c0392b", lw=1.8,
                            connectionstyle="arc3,rad=0.3"))

ax.set_title("Rysunek 3.1. Architektura środowiska badawczego (przepływ żądania i rozmieszczenie komponentów)",
             fontsize=11, pad=12)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_architecture.png"), dpi=150, bbox_inches="tight")
print("Zapisano", os.path.join(OUT, "fig_architecture.png"))
