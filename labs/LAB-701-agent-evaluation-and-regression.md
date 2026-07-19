---
id: lab.701.agent-evaluation-and-regression
title: LAB-701 — Avaliação de agentes e regressão
lang: pt-BR
status: review
version: 0.1.0
estimated_time: 5h
---

# LAB-701 — Avaliação de agentes e regressão

## Hipótese

Uma suíte versionada, multidimensional e orientada por hard gates detecta regressões que uma média única não revela.

## Missão

Construir um evaluation harness local que compare baseline e candidato, aplique graders independentes e produza uma decisão de release auditável.

## Cenários obrigatórios

| ID | Condição | Resultado obrigatório |
|---|---|---|
| E1 | candidato melhora casos normais sem falha crítica | melhoria registrada |
| E2 | nova violação de política em caso crítico | release bloqueado |
| E3 | resposta correta com trajetória proibida | caso reprovado |
| E4 | schema inválido | falha determinística |
| E5 | groundedness abaixo do threshold | regressão registrada |
| E6 | custo aumenta acima do budget | release bloqueado ou exceção aprovada |
| E7 | p95 de latência excede limite | regressão operacional |
| E8 | grader heurístico discorda do determinístico | discordância registrada |
| E9 | caso de holdout contaminado | execução inválida |
| E10 | resultado varia entre repetições | variância reportada |
| E11 | baseline falha e candidato corrige | melhoria confirmada |
| E12 | médias melhoram, mas caso crítico piora | hard gate prevalece |

## Dataset mínimo

Crie pelo menos 20 casos:

- 6 core;
- 4 regression;
- 4 adversarial;
- 4 holdout;
- 2 operational.

Cada caso deve declarar:

```yaml
case_id: eval-001
dataset_version: 2026.07.1
partition: regression
severity: critical
tags: [security, tool-policy]
source_refs: [incident:INC-004]
grader_policy: grader-set:v2
```

## Graders obrigatórios

1. schema;
2. terminal state;
3. ação proibida;
4. cobertura de fatos obrigatórios;
5. groundedness heurístico;
6. custo;
7. latência;
8. trajetória;
9. consistência entre repetições;
10. decisão agregada por hard gate.

## Procedimento

1. Fixe baseline, candidato, dataset e grader set.
2. Valide schema e proveniência dos casos.
3. Execute ambos nas mesmas entradas e parâmetros.
4. Registre resultado final, trajetória, custo, latência e terminal state.
5. Aplique graders individualmente.
6. Compare por caso, dimensão, severidade e partição.
7. Calcule regressões, melhorias e casos inalterados.
8. Aplique hard gates antes da média ponderada.
9. Gere relatório JSON e resumo Markdown.
10. Execute todos os cenários adversariais.

## Hard gates mínimos

```yaml
policy_violations: 0
cross_scope_leaks: 0
duplicate_effects: 0
critical_case_pass_rate: 1.0
invalid_cases: 0
```

## Thresholds mínimos

```yaml
overall_pass_rate: 0.90
groundedness_rate: 0.90
max_cost_regression_pct: 10
max_p95_latency_regression_pct: 15
max_grader_disagreement_rate: 0.10
```

## Comandos

```bash
python examples/evaluation_harness.py --self-test
python tests/validate_repository.py
```

## Evidências

- dataset versionado;
- configuração de graders;
- saída por caso;
- comparação baseline/candidato;
- métricas agregadas;
- lista de regressões;
- decisão de release;
- relatório de variância;
- reflexão sobre limitações.

## Critérios de aprovação

| Critério | Meta |
|---|---:|
| cenários obrigatórios executados | 12/12 |
| violações críticas toleradas | 0 |
| casos sem proveniência | 0 |
| regressões não classificadas | 0 |
| hard gates aplicados antes da média | 100% |
| relatórios com justificativa | 100% |
| segredos em logs | 0 |

## Testes adversariais

- alterar a severidade de um caso depois da execução;
- remover evidência de uma falha crítica;
- usar resultado do candidato como expected output;
- contaminar holdout com identificadores exclusivos;
- fazer grader aceitar texto sem evidência;
- esconder custo de retries;
- calcular p95 com amostra insuficiente sem alerta;
- usar versões diferentes de dataset entre baseline e candidato;
- descartar execuções ruins como outliers sem regra prévia;
- permitir que média compense violação crítica.

## Stop conditions

Pare imediatamente quando houver:

- schema incompatível;
- dataset ou grader set não versionado;
- baseline e candidato em condições diferentes;
- caso crítico sem hard gate;
- evidência adulterada;
- segredo em log;
- tentativa de reclassificar falha após o resultado.

## Entrega Premium Elite

A entrega final deve permitir que outra pessoa execute a suíte, obtenha os mesmos cálculos e compreenda exatamente por que o candidato foi aprovado ou bloqueado.
