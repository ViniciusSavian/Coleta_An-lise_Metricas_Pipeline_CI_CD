#!/usr/bin/env python3
"""
Coleta métricas reais de execução do pipeline CI/CD via API do GitHub.

Uso:
    export GITHUB_TOKEN=<seu_token>
    python scripts/collect_metrics.py

Saída:
    Entregaveis/metrics.csv
    Entregaveis/metrics.json
"""

import csv
import json
import os
import sys
import time
import zipfile
import io
from datetime import datetime

import requests

# ── Configuração ──────────────────────────────────────────────────────────────

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO_OWNER   = "ViniciusSavian"
REPO_NAME    = "Coleta_An-lise_Metricas_Pipeline_CI_CD"
WORKFLOW_FILE = "ci.yml"

BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Entregaveis")

# ── Helpers ───────────────────────────────────────────────────────────────────


def _get(url: str, params: dict = None) -> dict:
    """GET com tratamento de rate limit."""
    for attempt in range(3):
        resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        if resp.status_code == 403 and "rate limit" in resp.text.lower():
            reset = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
            wait  = max(reset - int(time.time()), 10)
            print(f"  Rate limit atingido. Aguardando {wait}s...")
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError(f"Falha após 3 tentativas: GET {url}")


def _parse_duration(started_at: str, completed_at: str):
    """Retorna duração em segundos ou None."""
    if not started_at or not completed_at:
        return None
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    try:
        delta = (
            datetime.strptime(completed_at, fmt)
            - datetime.strptime(started_at, fmt)
        )
        return int(delta.total_seconds())
    except ValueError:
        return None


# ── Coleta principal ──────────────────────────────────────────────────────────


def get_workflow_runs() -> list:
    """Retorna todas as execuções do workflow, paginadas."""
    runs, page = [], 1
    print(f"Buscando execuções do workflow '{WORKFLOW_FILE}'...")
    while True:
        data = _get(
            f"{BASE_URL}/actions/workflows/{WORKFLOW_FILE}/runs",
            params={"per_page": 100, "page": page},
        )
        batch = data.get("workflow_runs", [])
        if not batch:
            break
        runs.extend(batch)
        print(f"  Página {page}: {len(batch)} execuções")
        if len(batch) < 100:
            break
        page += 1
    return runs


def get_jobs(run_id: int) -> list:
    """Retorna os jobs de uma execução."""
    data = _get(f"{BASE_URL}/actions/runs/{run_id}/jobs")
    return data.get("jobs", [])


def get_test_metrics_from_artifact(run_id: int) -> dict:
    """Tenta baixar e ler o artefato test_metrics.json de uma execução."""
    default = {"test_count": 0, "test_passed": 0, "test_failures": 0, "test_duration": 0.0}
    try:
        data = _get(f"{BASE_URL}/actions/runs/{run_id}/artifacts")
        artifacts = data.get("artifacts", [])

        # Procura pelo artefato de métricas de teste
        target = None
        for art in artifacts:
            if art["name"].startswith("test-metrics-"):
                target = art
                break

        if not target:
            return default

        # Baixa o zip do artefato
        download_url = target["archive_download_url"]
        resp = requests.get(download_url, headers=HEADERS, timeout=30)
        if resp.status_code != 200:
            return default

        # Extrai e lê o JSON
        with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
            with zf.open("test_metrics.json") as f:
                metrics = json.load(f)
        return metrics

    except Exception as exc:
        print(f"    [WARN] Não foi possível ler artefato de run {run_id}: {exc}")
        return default


# ── Montagem dos registros CSV/JSON ───────────────────────────────────────────


def build_records(runs: list) -> list:
    """Monta lista de registros com todas as métricas."""
    records = []

    for run in runs:
        run_id      = run["id"]
        run_number  = run["run_number"]
        commit_sha  = run["head_sha"][:8]
        head_commit = run.get("head_commit") or {}
        commit_msg  = head_commit.get("message", "").split("\n")[0][:120]
        status      = run["conclusion"] or run["status"]
        timestamp   = run["created_at"]
        workflow_duration = _parse_duration(run["created_at"], run["updated_at"])

        print(f"  Run #{run_number} (ID {run_id}) — {status}")

        # Tenta obter contagem de testes do artefato
        test_meta = get_test_metrics_from_artifact(run_id)
        time.sleep(0.3)

        # Jobs e steps
        jobs = get_jobs(run_id)
        time.sleep(0.3)

        for job in jobs:
            job_name     = job["name"]
            job_status   = job["conclusion"] or job["status"]
            job_duration = _parse_duration(job.get("started_at"), job.get("completed_at"))

            # Steps do job
            steps = job.get("steps", [])
            steps_detail = {
                s["name"]: _parse_duration(s.get("started_at"), s.get("completed_at"))
                for s in steps
            }

            records.append({
                "run_id":           run_id,
                "run_number":       run_number,
                "commit_sha":       commit_sha,
                "commit_message":   commit_msg,
                "status":           status,
                "workflow_duration": workflow_duration,
                "job_name":         job_name,
                "job_status":       job_status,
                "job_duration":     job_duration,
                "test_count":       test_meta.get("test_count", 0),
                "test_failures":    test_meta.get("test_failures", 0),
                "test_duration":    test_meta.get("test_duration", 0.0),
                "timestamp":        timestamp,
                "steps_detail":     json.dumps(steps_detail),
            })

    return records


# ── Persistência ──────────────────────────────────────────────────────────────

CSV_FIELDS = [
    "run_id", "run_number", "commit_sha", "commit_message",
    "status", "workflow_duration", "job_name", "job_status",
    "job_duration", "test_count", "test_failures", "test_duration",
    "timestamp", "steps_detail",
]


def save_csv(records: list, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(records)
    print(f"\nCSV salvo em: {path}  ({len(records)} linhas)")


def save_json(records: list, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Remove steps_detail do JSON para evitar dupla serialização
    clean = [{k: v for k, v in r.items() if k != "steps_detail"} for r in records]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(clean, f, indent=2, ensure_ascii=False)
    print(f"JSON salvo em: {path}")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if not GITHUB_TOKEN:
        print(
            "ERRO: variável GITHUB_TOKEN não definida.\n"
            "Defina com:  export GITHUB_TOKEN=ghp_<seu_token>\n",
            file=sys.stderr,
        )
        sys.exit(1)

    runs = get_workflow_runs()
    if not runs:
        print("Nenhuma execução encontrada.")
        sys.exit(0)

    print(f"\nTotal de execuções: {len(runs)}")
    print("Coletando métricas de jobs e artefatos...\n")

    records = build_records(runs)

    csv_path  = os.path.join(OUTPUT_DIR, "metrics.csv")
    json_path = os.path.join(OUTPUT_DIR, "metrics.json")

    save_csv(records, csv_path)
    save_json(records, json_path)

    print(f"\n✓ Coleta concluída — {len(records)} registros.")


if __name__ == "__main__":
    main()
