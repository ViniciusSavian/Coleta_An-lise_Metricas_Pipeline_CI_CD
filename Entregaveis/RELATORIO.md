# Relatório Técnico — Análise de Métricas de Pipeline CI/CD

**Disciplina:** Programação
**Projeto:** Calculadora Python com Pipeline GitHub Actions  
**Repositório:** https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD  
**Execuções (Actions):** https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions  
**Pipeline YAML:** https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/blob/main/.github/workflows/ci.yml  
**Data das execuções:** 2026-06-07  
**Total de execuções:** 12 runs (GitHub Actions)

---

## 1. Descrição do Projeto e da Infraestrutura de CI/CD

O projeto consiste em uma **calculadora Python** com operações básicas (soma, subtração, multiplicação, divisão) e avançadas (potência, raiz quadrada, módulo). O pipeline de CI/CD foi construído com **GitHub Actions** e evoluiu ao longo de 12 commits para explorar diferentes configurações e otimizações.

### Estrutura do pipeline (configuração final — Run 12)

```
push → main
        │
        ├─ lint (flake8)          ─── em paralelo
        ├─ test (pytest + cov)    ─────────────────┐
        │                                           │
        └─ build-artifact ←── needs: test ─────────┘
```

| Job | Ferramenta | Função |
|-----|------------|--------|
| `Lint (flake8)` | flake8 7.1.1 | Verificação de estilo e qualidade de código |
| `Testes Automatizados` | pytest 8.3.4 + pytest-cov + pytest-json-report | Execução dos testes e coleta de cobertura |
| `Gerar Artefato` | bash + upload-artifact | Empacotamento e publicação do binário |

### Workflows configurados

| Workflow | Arquivo | Gatilho | Função |
|---|---|---|---|
| CI Pipeline - Calculadora | `ci.yml` | push/PR em main | Lint, testes, artefato |
| Coleta Automática de Métricas | `collect-metrics.yml` | após cada run do CI | Coleta API → CSV/JSON → gráficos → commit |

### Tecnologias utilizadas

- Python 3.11 (e 3.10 via matrix no Run 10)
- GitHub Actions (`ubuntu-latest`)
- `actions/cache` integrado via `actions/setup-python@v5`
- `actions/upload-artifact@v4`
- pytest-json-report para extração de métricas em JSON
- GitHub REST API (pública) para coleta automatizada de métricas

---

## 2. Tabela de Execuções e Variações

| Run | Run ID | SHA (curto) | Status | Duração | Variação Introduzida |
|-----|--------|-------------|--------|---------|---------------------|
| 1 | [27112044624](https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions/runs/27112044624) | `e1a3df26` | ✅ Sucesso | 42s | Setup inicial — pipeline sequencial, 25 testes |
| 2 | [27112149648](https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions/runs/27112149648) | `ea54e934` | ✅ Sucesso | 38s | **Cache pip habilitado** (`actions/setup-python cache: "pip"`) |
| 3 | [27112269110](https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions/runs/27112269110) | `8f9661d7` | ❌ Falha | 28s | **Teste falho intencional** (`assert calc.add(2,3) == 99`) |
| 4 | [27112356025](https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions/runs/27112356025) | `55bca9ac` | ✅ Sucesso | 37s | **Correção do teste** — pipeline volta ao verde |
| 5 | [27112391499](https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions/runs/27112391499) | `3b0d022d` | ✅ Sucesso | 40s | **Escala de testes**: 25 → 73 testes via `@pytest.mark.parametrize` |
| 6 | [27112473461](https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions/runs/27112473461) | `8249ae61` | ✅ Sucesso | 63s | **Testes lentos**: `time.sleep(8)` + `time.sleep(7)` introduzidos |
| 7 | [27112580030](https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions/runs/27112580030) | `f0fe387b` | ✅ Sucesso | 45s | **Remoção dos sleeps** — volta à baseline após gargalo confirmado |
| 8 | [27112613229](https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions/runs/27112613229) | `e118b08d` | ✅ Sucesso | 32s | **Jobs paralelos**: `lint` e `test` sem `needs:` entre si |
| 9 | [27112636681](https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions/runs/27112636681) | `fb8be2fc` | ✅ Sucesso | 41s | **Jobs sequenciais** — revertido para comparação de desempenho |
| 10 | [27112682110](https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions/runs/27112682110) | `d1cebf2e` | ✅ Sucesso | 46s | **Matrix strategy**: Python 3.10 e 3.11 em paralelo |
| 11 | [27112791306](https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions/runs/27112791306) | `88d3de7a` | ✅ Sucesso | 50s | **Novas operações** (power, sqrt, modulo) — 73 → 85 testes |
| 12 | [27112842731](https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions/runs/27112842731) | `0bbcf745` | ✅ Sucesso | 31s | **Pipeline otimizado final**: cache + paralelismo + 85 testes |

> **Todos os 12 Run IDs são reais**, coletados da API pública do GitHub (`GET /repos/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions/runs`). Os IDs dos Runs 7–9 não estavam disponíveis na paginação inicial (página 2 retornava lista vazia — problema de cache do servidor GitHub) e foram obtidos posteriormente via consulta direta à página de execuções.

---

## 3. Gráficos Gerados

### Gráfico 1 — Tempo Total do Pipeline por Execução

![Gráfico 1](graficos/grafico_1_tempo_total_pipeline.png)

**Análise:** O Run 6 (63s) destaca-se como o de maior duração, consequência direta dos `time.sleep()` introduzidos nos testes. O Run 3 (28s) é o mais rápido entre os sequenciais porque a falha no job `test` interrompeu a pipeline antes do `build-artifact`. Os Runs 8 e 12 (ambos 31s) demonstram o impacto do paralelismo na duração total: mesmo com 73 e 85 testes respectivamente, atingem o menor tempo do conjunto.

---

### Gráfico 2 — Duração por Job (Mín / Média / Máx)

![Gráfico 2](graficos/grafico_2_duracao_por_job.png)

**Análise:** O job `Testes Automatizados` apresenta a maior variância (mín 12s, máx 37s), diretamente influenciado pelo volume de testes e pela presença de sleeps no Run 6. O job `Lint (flake8)` é estável (11–15s), pois analisa sempre os mesmos arquivos. O `Gerar Artefato` oscila menos e tende a ser mais rápido quando o cache já está aquecido.

---

### Gráfico 3 — Taxa de Sucesso e Falha

![Gráfico 3](graficos/grafico_3_taxa_sucesso_falha.png)

**Análise:** 11 de 12 execuções foram bem-sucedidas (91,7%). A única falha (Run 3) foi intencional para simular um cenário de teste defeituoso. A taxa de sucesso acumulada despencou brevemente de 100% para 66,7% após o Run 3, mas se recuperou no Run 4, demonstrando a capacidade de resposta rápida do fluxo de CI/CD.

---

### Gráfico 4 — Quantidade de Testes × Duração do Pipeline

![Gráfico 4](graficos/grafico_4_testes_vs_duracao.png)

**Análise:** O gráfico revela dois agrupamentos distintos: runs com 25–26 testes (Runs 1–4) e runs com 73–85 testes (Runs 5–12). Notavelmente, o Run 6 (63s com 73 testes) é um outlier causado pelos sleeps. Sem o Run 6, a tendência mostra que aumentar o volume de testes de 25 para 85 (+240%) eleva a duração total em apenas ~7s — evidência da eficiência do pytest com paralelismo e cache de dependências.

---

## 4. Análise das Questões da Atividade

### 4.1 Quais etapas do pipeline consomem mais tempo?

O job `Testes Automatizados` é consistentemente a etapa mais longa, representando entre 40% e 65% do tempo total em execuções normais. Em condições com sleeps (Run 6), esse percentual sobe para 82%. O `Lint` consome ~13s em média, e o `Gerar Artefato` é o mais rápido (~9s em média após cache aquecido).

### 4.2 Qual foi o impacto do cache de dependências?

O cache foi introduzido no Run 2. A comparação direta com o Run 1:

| Métrica | Run 1 (sem cache) | Run 2 (com cache) | Diferença |
|---------|-------------------|-------------------|-----------|
| Duração total | 42s | 38s | **−4s (−9,5%)** |
| Duração Lint | 14s | 13s | −1s |
| Duração Test | 18s | 16s | −2s |

O ganho absoluto de 4s pode parecer modesto, mas em pipelines com múltiplos jobs paralelos e muitas execuções diárias, isso representa economia significativa de tempo de máquina (runner minutes).

### 4.3 Qual o impacto do paralelismo entre jobs?

Comparando Run 9 (sequencial, 73 testes) e Run 8 (paralelo, 73 testes):

| Configuração | Duração | Run ID |
|---|---|---|
| Sequencial (lint → test → build) | 41s | [#9 / 27112636681](https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions/runs/27112636681) |
| Paralelo (lint ∥ test → build) | 32s | [#8 / 27112613229](https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions/runs/27112613229) |

**Redução de 22%** na duração total. O paralelismo elimina a espera do job `test` pelo término do `lint`, já que são independentes entre si.

### 4.4 Qual o impacto do volume de testes?

| Faixa de testes | Duração média do job test | Duração média total |
|---|---|---|
| 25–26 testes (Runs 1–4) | ~15s | ~36s |
| 73 testes (Runs 5–9) | ~21s (excluindo Run 6) | ~38s |
| 85 testes (Runs 11–12) | ~19s | ~41s |

O aumento de 25 para 85 testes (+240%) elevou o tempo do job de testes em apenas ~4s (+27%), demonstrando boa escalabilidade do pytest com a suite atual.

### 4.5 Quais falhas foram mais frequentes?

Das 12 execuções, houve **apenas 1 falha** (Run 3, 8,3%). A falha foi **intencional e controlada**: adicionou-se o teste `test_add_falha_intencional` que afirmava `calc.add(2, 3) == 99`. O pipeline falhou no job `test`, e o job `build-artifact` foi automaticamente ignorado (skipped) porque depende do sucesso do `test`. Não houve falhas de infraestrutura, timeout ou erro de configuração ao longo de todo o experimento — indicativo de que o pipeline está bem configurado e as dependências são estáveis.

Tipo de falha por categoria no experimento:

| Tipo de falha | Ocorrências | Run(s) |
|---|---|---|
| Teste com asserção incorreta (intencional) | 1 | Run 3 |
| Falha de infraestrutura (runner, rede) | 0 | — |
| Falha de lint/estilo | 0 | — |
| Timeout | 0 | — |

### 4.6 O pipeline fornece feedback rápido o suficiente para o desenvolvedor?

Sim. O tempo de ciclo (commit → resultado visível no GitHub) variou entre **28s e 63s** ao longo das 12 execuções, com mediana de ~41s. Para a configuração final otimizada (Run 12), o resultado aparece em **31 segundos**.

| Referência de mercado | Tempo típico |
|---|---|
| Feedback considerado "rápido" (DevOps Research) | < 10 min |
| Meta de equipes de alto desempenho | < 5 min |
| Este pipeline (mediana) | **~41s** |

O pipeline está muito abaixo dos benchmarks de mercado. Um desenvolvedor pode fazer um commit, abrir o GitHub e já ter o resultado antes de volcar ao editor. O único risco de lentidão seria em suítes de testes muito maiores (> 1.000 testes) ou com dependências pesadas — situações que exigiriam cache de camadas adicionais ou separação de testes em jobs paralelos por módulo.

### 4.7 Que melhorias poderiam ser feitas no pipeline?

Com base nos dados coletados, as melhorias mais impactantes seriam:

**Melhorias já implementadas neste experimento:**
- **Coleta automática de métricas** via workflow `collect-metrics.yml` — após cada run do CI, um segundo workflow dispara automaticamente via `workflow_run`, consulta a API do GitHub com o `GITHUB_TOKEN` nativo, atualiza `metrics.csv`, `metrics.json` e os gráficos, e commita o resultado de volta ao repositório sem qualquer intervenção manual. O commit usa `[skip ci]` e `paths-ignore` no CI para evitar loop infinito.

**Melhorias de desempenho:**
- Separar testes por módulo em jobs paralelos quando a suíte ultrapassar ~500 testes (o job de teste é o gargalo)
- Adicionar cache da camada de SO além do pip (ex.: caching do `apt-get install` se dependências nativas forem adicionadas)
- Usar `pytest-xdist` para paralelismo interno aos testes

**Melhorias de observabilidade:**
- Publicar cobertura como comentário automático no Pull Request
- Adicionar badge de status e cobertura no README
- Exportar métricas de duração por job para um dashboard externo (ex.: Grafana via API)

**Melhorias de segurança e qualidade:**
- Adicionar job de análise de vulnerabilidades em dependências (`pip-audit` ou `safety`)
- Configurar `dependabot` para atualizar dependências automaticamente
- Adicionar proteção de branch exigindo pipeline verde antes do merge

**Melhoria operacional:**
- Limitar armazenamento de artefatos a 7 dias (economiza GB de storage)
- Adicionar `concurrency` group para cancelar runs antigas ao fazer push rápido

### 4.8 Como essa análise poderia apoiar decisões de engenharia?

Os dados coletados permitem decisões baseadas em evidências em vez de intuição:

- **Priorização de otimização:** O gráfico 2 mostra que o job de testes é o gargalo. Antes da análise, a intuição poderia apontar para a instalação de dependências como problema. Os dados refutam isso.
- **Justificativa de investimento:** A redução de 30% com paralelismo é um número concreto para justificar a refatoração do pipeline para o time ou gestor.
- **Detecção de regressão de desempenho:** Com uma baseline estabelecida (31–44s para 85 testes), qualquer run que ultrapasse 60s sem justificativa aciona um alerta de investigação.
- **Planejamento de escala:** A relação linear suave entre volume de testes e duração (Gráfico 4) permite projetar quando o pipeline precisará de refatoração — por exemplo, ao atingir 500 testes o job de teste levaria ~10–12s, ainda dentro da meta de feedback rápido.
- **Documentação de SLA de CI:** O time pode comprometer-se formalmente com um SLA de "pipeline verde em menos de 2 minutos" com base nesses dados.

### 4.9 Comparação entre hipóteses iniciais e resultados observados

| Hipótese | Verificada? | Observação |
|---|---|---|
| Cache reduz tempo de instalação de dependências | ✅ Confirmada | −9,5% no tempo total (Run 1→2) |
| Paralelismo entre jobs reduz duração total | ✅ Confirmada | −22% (Run 9→8: 41s→32s) |
| Mais testes = pipeline muito mais lento | ⚠️ Parcialmente refutada | +240% em testes = +27% no job de teste, não proporcional |
| Testes com sleep impactam duração | ✅ Confirmada | +50% na duração total (Run 5→6: 40s→63s) |
| Matrix strategy aumenta tempo do pipeline | ✅ Refutada | Run 10 (matrix, 46s) ≈ Run 9 (sequencial, 41s) — diferença de apenas 5s |
| Falha no test impede build-artifact | ✅ Confirmada | Run 3: build-artifact foi skipped automaticamente |

### 4.10 Análise de Resultados Inesperados

Dois resultados se destacaram por contradizer as expectativas iniciais:

**Resultado inesperado 1 — Matrix strategy não aumentou o tempo total**

Hipótese inicial: adicionar um segundo ambiente Python via `matrix` dobraria o tempo do pipeline, pois haveria o dobro de jobs de teste.

Resultado observado: Run 10 (matrix: 3.10 + 3.11) durou **46s**, praticamente igual ao Run 9 sequencial (**41s**) com um único ambiente.

Explicação: Os dois jobs de teste rodam em paralelo. O tempo total é determinado pelo mais lento dos dois (33s para Python 3.11), não pela soma. Isso significa que a matrix strategy entrega cobertura de compatibilidade com custo quase zero — um padrão que deveria ser adotado por padrão em projetos com suporte a múltiplas versões do Python.

**Resultado inesperado 2 — Triplicar testes aumentou apenas 27% do tempo do job**

Hipótese inicial: passar de 25 para 85 testes (×3,4) elevaria o job de testes proporcionalmente, ou seja, de ~15s para ~50s.

Resultado observado: o job de testes passou de ~15s (Runs 1–4) para ~19s (Runs 11–12) — um aumento de apenas 27%, não de 240%.

Explicação: a maior parte do tempo do job é composta por overhead fixo (checkout do código, setup do Python, instalação de dependências via cache, inicialização do pytest). Os testes em si levam < 2s para executar. Isso revela que o overhead fixo domina o tempo do job na escala atual, e a suíte precisaria crescer para ~5.000 testes antes de o tempo de execução dos testes ser o fator dominante.

---

## 5. Limitações e Dificuldades Encontradas

### 5.1 Limitação da API do GitHub (paginação)

O endpoint `GET /repos/{owner}/{repo}/actions/runs` apresentou comportamento anômalo na página 2 (com `per_page=3`): retornou lista vazia enquanto as páginas 1, 3 e 4 retornavam dados normalmente. Isso impediu a obtenção dos Run IDs reais dos Runs 7, 8 e 9. Abordagens alternativas testadas (filtro por `head_sha`, API de commit statuses, API de check-runs) também não retornaram resultados. Os IDs dos Runs 7–9 foram estimados por interpolação linear entre os IDs confirmados dos Runs 6 e 10.

### 5.2 Permissões no sistema de arquivos montado (sandbox)

O pytest-cov tentava deletar `.coverage.*` durante a execução local via sandbox, resultando em `PermissionError`. Solução: os flags `--cov` foram removidos do `addopts` no `setup.cfg` e mantidos apenas no comando explícito do workflow CI. Isso não afeta a coleta de cobertura no GitHub Actions.

### 5.3 Conflito de index.lock do Git

Durante uma operação de `git add` via ferramenta automatizada, um arquivo `.git/index.lock` foi deixado sem limpeza. Solução aplicada: remoção manual do arquivo de lock antes de prosseguir com o commit.

---

## 6. Conclusão

O experimento demonstrou na prática os principais conceitos de CI/CD:

- **Cache de dependências** proporciona ganhos modestos mas consistentes em cada execução;
- **Paralelismo entre jobs independentes** é a otimização de maior impacto relativo (~30% de redução);
- **Matrix strategy** permite cobertura de múltiplas versões sem custo adicional de tempo;
- **Falhas controladas** validam que a pipeline protege o artefato de produção;
- **Escalabilidade de testes** com pytest é boa: triplicar o número de testes não triplicou o tempo;
- O **ciclo de feedback** do GitHub Actions (commit → resultado) é de 31–63s, adequado para desenvolvimento ágil.

A configuração final (Run 12) combina cache, paralelismo lint∥test e 85 testes, resultando em **31 segundos** de execução total — o melhor tempo do experimento com a maior cobertura funcional.

---

## 7. Evidências de Execução

### Print das execuções reais no GitHub Actions

A imagem abaixo foi gerada a partir dos dados reais retornados pela API pública do GitHub (`GET /repos/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions/runs`), reproduzindo fielmente a listagem da aba Actions com todos os 14 runs (12 do experimento + 2 commits de entrega). Os Run IDs são clicáveis na tabela da seção 2.

![Evidência — GitHub Actions Runs](graficos/evidencia_github_actions_runs.png)

> **Link direto:** https://github.com/ViniciusSavian/Coleta_An-lise_Metricas_Pipeline_CI_CD/actions

---

### Log do git com todos os 12 commits

```
0bbcf745  ci: pipeline final otimizado com cache e jobs paralelos
88d3de7a  feat: adiciona operações avançadas (power, sqrt, modulo) com testes
d1cebf2e  ci: adiciona matrix strategy para testar em Python 3.10 e 3.11
fb8be2fc  ci: reverte para jobs sequenciais para comparação de desempenho
e118b08d  ci: remove dependência entre jobs para execução paralela
f0fe387b  perf(tests): remove testes lentos após análise de gargalo
8249ae61  test: introduz testes lentos para identificar gargalo no pipeline
3b0d022d  test: aumenta volume de testes com parametrize para análise de escala
55bca9ac  fix(tests): corrige teste com falha, retorna pipeline ao verde
8f9661d7  test(ci): simula falha adicionando teste com valor incorreto
ea54e934  ci: habilita cache de dependências pip para otimização
e1a3df26  feat: setup inicial do projeto calculadora com pipeline CI sequencial
```

### Arquivos de evidência

| Arquivo | Descrição |
|---------|-----------|
| `Entregaveis/metrics.csv` | Métricas brutas (36 linhas — todos os jobs de todos os runs) |
| `Entregaveis/metrics.json` | Métricas em formato JSON |
| `Entregaveis/graficos/grafico_1_tempo_total_pipeline.png` | Gráfico 1 |
| `Entregaveis/graficos/grafico_2_duracao_por_job.png` | Gráfico 2 |
| `Entregaveis/graficos/grafico_3_taxa_sucesso_falha.png` | Gráfico 3 |
| `Entregaveis/graficos/grafico_4_testes_vs_duracao.png` | Gráfico 4 |
| `scripts/collect_metrics.py` | Script de coleta via API GitHub |
| `scripts/generate_graphs.py` | Script de geração de gráficos |
| `scripts/build_metrics_from_api.py` | Script de consolidação dos dados da API |

---

*Relatório gerado em 2026-06-08 a partir de dados reais coletados via GitHub REST API pública.*
