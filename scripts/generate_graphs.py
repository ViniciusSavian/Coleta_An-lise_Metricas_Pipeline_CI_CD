#!/usr/bin/env python3
"""
Gera os quatro gráficos obrigatórios a partir das métricas coletadas.

Pré-requisito:
    pip install pandas matplotlib

Uso:
    python scripts/generate_graphs.py

Entrada:   Entregaveis/metrics.csv
Saída:     Entregaveis/graficos/grafico_*.png
"""

import os
import sys
import json
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

matplotlib.use("Agg")  # backend sem GUI

# ── Paths ────────────────────────────────────────────────────────────────────

ROOT_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METRICS_CSV = os.path.join(ROOT_DIR, "Entregaveis", "metrics.csv")
GRAPHS_DIR  = os.path.join(ROOT_DIR, "Entregaveis", "graficos")

# ── Paleta ────────────────────────────────────────────────────────────────────

COLORS = {
    "success": "#2ecc71",
    "failure": "#e74c3c",
    "neutral": "#3498db",
    "accent":  "#9b59b6",
    "warn":    "#f39c12",
}

plt.rcParams.update({
    "figure.facecolor":  "#ffffff",
    "axes.facecolor":    "#f8f9fa",
    "axes.edgecolor":    "#dee2e6",
    "axes.labelcolor":   "#343a40",
    "xtick.color":       "#343a40",
    "ytick.color":       "#343a40",
    "text.color":        "#343a40",
    "grid.color":        "#dee2e6",
    "grid.linestyle":    "--",
    "grid.alpha":        0.7,
    "font.family":       "DejaVu Sans",
})


# ── Carga de dados ────────────────────────────────────────────────────────────


def load_data() -> pd.DataFrame:
    if not os.path.exists(METRICS_CSV):
        print(f"ERRO: arquivo não encontrado: {METRICS_CSV}")
        print("Execute primeiro: python scripts/collect_metrics.py")
        sys.exit(1)

    df = pd.read_csv(METRICS_CSV)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df.sort_values("run_number", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


# ── Gráfico 1: Tempo total do pipeline por execução ───────────────────────────


def grafico_1_tempo_total(df: pd.DataFrame) -> None:
    """Gráfico de barras: duração total do workflow por número de execução."""
    # Um registro por run (workflow_duration é o mesmo para todos os jobs do run)
    runs = (
        df.groupby("run_number")
        .agg(
            workflow_duration=("workflow_duration", "first"),
            status=("status", "first"),
            commit_sha=("commit_sha", "first"),
        )
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(14, 6))

    bar_colors = [
        COLORS["success"] if s == "success" else COLORS["failure"]
        for s in runs["status"]
    ]

    bars = ax.bar(runs["run_number"], runs["workflow_duration"], color=bar_colors, width=0.6)

    # Rótulos acima das barras
    for bar, dur, sha in zip(bars, runs["workflow_duration"], runs["commit_sha"]):
        if dur and dur > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 1,
                f"{int(dur)}s",
                ha="center", va="bottom", fontsize=8, color="#343a40",
            )

    # Legenda manual
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=COLORS["success"], label="Sucesso"),
        Patch(facecolor=COLORS["failure"], label="Falha"),
    ]
    ax.legend(handles=legend_elements, loc="upper right")

    ax.set_title("Gráfico 1 — Tempo Total do Pipeline por Execução", fontsize=14, pad=15)
    ax.set_xlabel("Número da Execução (Run Number)")
    ax.set_ylabel("Duração Total (segundos)")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)

    plt.tight_layout()
    path = os.path.join(GRAPHS_DIR, "grafico_1_tempo_total_pipeline.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  ✓ {path}")


# ── Gráfico 2: Tempo por job/etapa ────────────────────────────────────────────


def grafico_2_tempo_por_job(df: pd.DataFrame) -> None:
    """Gráfico de barras agrupadas: duração média por job."""
    job_stats = (
        df.groupby("job_name")
        .agg(
            duracao_media=("job_duration", "mean"),
            duracao_max=("job_duration", "max"),
            duracao_min=("job_duration", "min"),
        )
        .reset_index()
        .sort_values("duracao_media", ascending=False)
    )

    x   = range(len(job_stats))
    w   = 0.25
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar([i - w for i in x], job_stats["duracao_min"],   width=w, label="Mínimo",  color=COLORS["success"])
    ax.bar([i     for i in x], job_stats["duracao_media"], width=w, label="Média",   color=COLORS["neutral"])
    ax.bar([i + w for i in x], job_stats["duracao_max"],   width=w, label="Máximo",  color=COLORS["failure"])

    ax.set_xticks(list(x))
    ax.set_xticklabels(job_stats["job_name"], rotation=20, ha="right")
    ax.set_title("Gráfico 2 — Duração por Job (Mín / Média / Máx)", fontsize=14, pad=15)
    ax.set_xlabel("Nome do Job")
    ax.set_ylabel("Duração (segundos)")
    ax.legend()
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)

    plt.tight_layout()
    path = os.path.join(GRAPHS_DIR, "grafico_2_duracao_por_job.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  ✓ {path}")


# ── Gráfico 3: Taxa de sucesso e falha ────────────────────────────────────────


def grafico_3_taxa_sucesso_falha(df: pd.DataFrame) -> None:
    """Gráfico de pizza e linha de tendência combinados."""
    runs = df.drop_duplicates("run_number")[["run_number", "status"]].sort_values("run_number")

    contagem = runs["status"].value_counts()
    labels   = contagem.index.tolist()
    sizes    = contagem.values.tolist()
    cores    = [COLORS["success"] if l == "success" else COLORS["failure"] for l in labels]

    # Linha temporal de status (1=sucesso, 0=falha)
    runs["passou"] = (runs["status"] == "success").astype(int)
    taxa_acum = runs["passou"].expanding().mean() * 100

    fig, (ax_pizza, ax_linha) = plt.subplots(1, 2, figsize=(14, 6))

    # Pizza
    wedges, texts, autotexts = ax_pizza.pie(
        sizes, labels=labels, colors=cores,
        autopct="%1.1f%%", startangle=90, pctdistance=0.8,
    )
    for at in autotexts:
        at.set_fontsize(12)
    ax_pizza.set_title("Distribuição de Status", fontsize=13)

    # Linha acumulada
    ax_linha.plot(
        runs["run_number"], taxa_acum,
        marker="o", color=COLORS["neutral"], linewidth=2,
    )
    ax_linha.fill_between(runs["run_number"], taxa_acum, alpha=0.15, color=COLORS["neutral"])
    ax_linha.set_ylim(0, 105)
    ax_linha.set_title("Taxa de Sucesso Acumulada (%)", fontsize=13)
    ax_linha.set_xlabel("Número da Execução")
    ax_linha.set_ylabel("% Sucesso")
    ax_linha.yaxis.grid(True)
    ax_linha.set_axisbelow(True)
    ax_linha.xaxis.set_major_locator(ticker.MultipleLocator(1))

    fig.suptitle("Gráfico 3 — Taxa de Sucesso e Falha", fontsize=14, y=1.01)
    plt.tight_layout()
    path = os.path.join(GRAPHS_DIR, "grafico_3_taxa_sucesso_falha.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ {path}")


# ── Gráfico 4: Quantidade de testes × duração ────────────────────────────────


def grafico_4_testes_vs_duracao(df: pd.DataFrame) -> None:
    """Gráfico de dispersão: quantidade de testes vs. duração do workflow."""
    runs = (
        df.groupby("run_number")
        .agg(
            workflow_duration=("workflow_duration", "first"),
            test_count=("test_count", "max"),
            test_failures=("test_failures", "max"),
            status=("status", "first"),
        )
        .reset_index()
    )

    # Filtra runs com dados de teste disponíveis
    valid = runs[runs["test_count"] > 0]

    fig, ax = plt.subplots(figsize=(10, 6))

    scatter_colors = [
        COLORS["success"] if s == "success" else COLORS["failure"]
        for s in valid["status"]
    ]

    sc = ax.scatter(
        valid["test_count"],
        valid["workflow_duration"],
        c=scatter_colors,
        s=80,
        alpha=0.85,
        zorder=3,
    )

    # Rótulos de run_number
    for _, row in valid.iterrows():
        ax.annotate(
            f"#{int(row['run_number'])}",
            (row["test_count"], row["workflow_duration"]),
            textcoords="offset points", xytext=(5, 3),
            fontsize=8, color="#555",
        )

    # Linha de tendência (se houver dados suficientes)
    if len(valid) >= 3:
        import numpy as np
        z = np.polyfit(valid["test_count"], valid["workflow_duration"].fillna(0), 1)
        p = np.poly1d(z)
        xs = sorted(valid["test_count"])
        ax.plot(xs, [p(x) for x in xs], "--", color=COLORS["warn"], linewidth=1.5,
                label="Tendência")
        ax.legend()

    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=COLORS["success"],
               markersize=10, label="Sucesso"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=COLORS["failure"],
               markersize=10, label="Falha"),
    ]
    ax.legend(handles=legend_elements, loc="upper left")

    ax.set_title("Gráfico 4 — Quantidade de Testes × Duração do Pipeline", fontsize=14, pad=15)
    ax.set_xlabel("Quantidade de Testes Executados")
    ax.set_ylabel("Duração Total do Workflow (segundos)")
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)

    plt.tight_layout()
    path = os.path.join(GRAPHS_DIR, "grafico_4_testes_vs_duracao.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  ✓ {path}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(GRAPHS_DIR, exist_ok=True)
    print(f"Lendo dados de: {METRICS_CSV}\n")

    df = load_data()
    print(f"Registros carregados: {len(df)} linhas")
    print(f"Execuções únicas:     {df['run_number'].nunique()}\n")
    print("Gerando gráficos...\n")

    grafico_1_tempo_total(df)
    grafico_2_tempo_por_job(df)
    grafico_3_taxa_sucesso_falha(df)
    grafico_4_testes_vs_duracao(df)

    print(f"\n✓ Todos os gráficos salvos em: {GRAPHS_DIR}")


if __name__ == "__main__":
    main()
