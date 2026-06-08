# Coleta e Análise de Métricas — Pipeline CI/CD

Projeto da disciplina de Engenharia de Software.  
Experimento prático para medir e analisar o comportamento de um pipeline CI/CD
usando GitHub Actions com uma calculadora simples em Python.

## Estrutura do Projeto

```
.
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline principal do GitHub Actions
├── calculator/
│   ├── __init__.py
│   └── calculator.py           # Implementação da calculadora
├── tests/
│   ├── __init__.py
│   └── test_calculator.py      # Testes automatizados (pytest)
├── scripts/
│   ├── collect_metrics.py      # Coleta métricas via API do GitHub
│   └── generate_graphs.py      # Gera os 4 gráficos obrigatórios
├── Entregaveis/                 # Gerado após execução dos scripts
│   ├── metrics.csv
│   ├── metrics.json
│   ├── graficos/
│   └── RELATORIO.md
├── requirements.txt
└── setup.cfg
```

## Pipeline CI/CD

O pipeline (`ci.yml`) contém três jobs executados em sequência:

| Job             | Etapas principais                         |
|-----------------|-------------------------------------------|
| `lint`          | flake8 — análise estática do código       |
| `test`          | pytest + cobertura + coleta de métricas   |
| `build-artifact`| Geração e upload do artefato da aplicação |

## Como Reproduzir o Experimento

### 1. Pré-requisitos

```bash
python -m pip install -r requirements.txt
```

### 2. Executar testes localmente

```bash
pytest
```

### 3. Coletar métricas após as execuções no GitHub Actions

```bash
export GITHUB_TOKEN=ghp_<seu_token>
python scripts/collect_metrics.py
```

### 4. Gerar os gráficos

```bash
pip install pandas matplotlib
python scripts/generate_graphs.py
```

Os resultados serão gerados em `Entregaveis/`.

## Variações Controladas (12 execuções)

| Run | Variação | Objetivo |
|-----|----------|----------|
| 1   | Setup inicial — sequencial, sem cache | Baseline |
| 2   | Habilitar cache de dependências | Medir ganho com cache |
| 3   | Teste com falha proposital | Simular falha de build |
| 4   | Corrigir teste com falha | Retorno ao verde |
| 5   | Aumentar volume de testes | Impacto na duração |
| 6   | Teste lento (sleep) | Identificar gargalo |
| 7   | Remover teste lento | Comparação de performance |
| 8   | Jobs paralelos | Medir redução de tempo |
| 9   | Jobs sequenciais | Comparação com paralelo |
| 10  | Matrix strategy (Python 3.10 + 3.11) | Paralelismo de versões |
| 11  | Novas operações na calculadora | Crescimento da suite de testes |
| 12  | Pipeline final otimizado | Melhor configuração geral |

## Entregáveis

Ver pasta [`Entregaveis/`](./Entregaveis/).
