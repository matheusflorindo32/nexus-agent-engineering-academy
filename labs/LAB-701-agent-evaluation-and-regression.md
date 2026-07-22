---
id: lab.701.agent-evaluation-and-regression
title: LAB-701 — Avaliação de agentes e regressão
lang: pt-BR
status: review
version: 0.2.0
estimated_time: 6h
risk_level: medium
module: course.module.07-evaluation-engineering
---

# LAB-701 — Avaliação de agentes e regressão

## Hipótese

Uma suíte versionada, multidimensional, reproduzível e orientada por hard gates detecta regressões que uma média única, uma avaliação subjetiva ou um grader não calibrado pode ocultar.

## Missão

Construir um evaluation harness local que compare baseline e candidato sob as mesmas condições, avalie resultado e trajetória, quantifique variância e produza uma decisão de release auditável.

## Resultado final observável

Ao final, outra pessoa deverá conseguir executar o harness e obter:

- dataset e grader set identificados por versão e hash;
- resultados por caso e por dimensão;
- comparação baseline versus candidato;
- hard gates aplicados antes de qualquer média;
- variância e flakiness explícitas;
- decisão `approve`, `block` ou `manual_review` com justificativa;
- relatório JSON e resumo Markdown reproduzíveis.

## Ambiente e segurança

- execução local e offline;
- dados exclusivamente sintéticos;
- nenhuma chave de API obrigatória;
- nenhum dado pessoal ou segredo em dataset, logs ou relatórios;
- tempo máximo recomendado de 6 horas;
- timeout absoluto de 15 segundos por execução simulada.

## Baseline obrigatório

Implemente um baseline determinístico simples e registre:

- versão;
- configuração;
- commit;
- dataset;
- seed;
- hardware ou ambiente relevante;
- política de retries;
- custos abstratos ou simulados.

Baseline e candidato devem receber as mesmas entradas, budgets, seeds e condições operacionais.

## Dataset mínimo

Crie pelo menos 24 casos:

- 6 `core`;
- 5 `regression`;
- 5 `adversarial`;
- 4 `holdout`;
- 4 `operational`.

Cada caso deve declarar:

```yaml
case_id: eval-001
dataset_version: 2026.07.2
partition: regression
severity: critical
tags: [security, tool-policy]
source_refs: [incident:INC-004]
expected_invariants:
  - no_external_effect
  - terminal_state: blocked
grader_policy: grader-set:v3
```

O holdout não pode ser usado para ajustar prompt, threshold, regra ou grader.

## Graders obrigatórios

1. schema;
2. terminal state;
3. ação proibida;
4. invariantes de segurança;
5. cobertura de fatos obrigatórios;
6. groundedness heurístico;
7. custo total, incluindo retries;
8. latência;
9. trajetória;
10. consistência entre repetições;
11. concordância entre graders;
12. decisão agregada por hard gate.

Grader por modelo, quando usado, precisa de versão, prompt, amostra de calibração, taxa de discordância e revisão humana dos casos críticos.

## Cenários obrigatórios

| ID | Condição | Resultado obrigatório |
|---|---|---|
| E1 | candidato melhora casos normais sem falha crítica | melhoria registrada |
| E2 | nova violação de política crítica | release bloqueado |
| E3 | resposta correta com trajetória proibida | caso reprovado |
| E4 | schema inválido | falha determinística |
| E5 | groundedness abaixo do threshold | regressão registrada |
| E6 | custo acima do budget | bloqueio ou exceção humana documentada |
| E7 | p95 acima do limite | regressão operacional |
| E8 | graders discordam | `manual_review` |
| E9 | holdout contaminado | execução inválida |
| E10 | resultado varia entre repetições | variância e flakiness reportadas |
| E11 | baseline falha e candidato corrige | melhoria confirmada |
| E12 | média melhora, caso crítico piora | hard gate prevalece |
| E13 | dataset muda entre execuções | comparação inválida |
| E14 | severidade alterada após resultado | evidência adulterada e release bloqueado |
| E15 | retries ocultos reduzem aparente custo | custo real recalculado |

## Procedimento

1. fixe baseline, candidato, dataset, grader set, seed e budgets;
2. valide schema, hashes e proveniência;
3. separe development, regression, adversarial, holdout e operational;
4. execute baseline e candidato nas mesmas condições;
5. repita casos estocásticos pelo menos cinco vezes;
6. registre resposta, trajetória, tools, custo, latência e terminal state;
7. aplique graders individualmente;
8. compare por caso, dimensão, severidade e partição;
9. calcule regressões, melhorias, flakiness e discordância;
10. aplique hard gates antes da média ponderada;
11. gere relatório JSON e resumo Markdown;
12. peça reprodução independente.

## Hard gates mínimos

```yaml
policy_violations: 0
cross_scope_leaks: 0
duplicate_effects: 0
critical_case_pass_rate: 1.0
invalid_cases: 0
holdout_contamination: 0
missing_evidence_for_critical_cases: 0
```

## Thresholds mínimos

```yaml
overall_pass_rate: 0.90
groundedness_rate: 0.90
max_cost_regression_pct: 10
max_p95_latency_regression_pct: 15
max_grader_disagreement_rate: 0.10
max_flaky_case_rate: 0.05
```

## Métricas obrigatórias

- pass rate geral e por severidade;
- critical pass rate;
- groundedness;
- policy violation rate;
- custo por sucesso;
- p50 e p95 de latência;
- regressões e melhorias por caso;
- grader disagreement rate;
- flaky case rate;
- trajectory violation rate;
- cobertura do dataset por risco e capability.

## Comandos

```bash
python examples/evaluation_harness.py --self-test
python tests/validate_repository.py
```

## Evidências

- dataset versionado e hash;
- configuração e calibração dos graders;
- versões de baseline e candidato;
- saída por caso e repetição;
- comparação por dimensão;
- métricas agregadas com denominadores;
- lista de regressões e casos flaky;
- decisão de release;
- limitações e risco residual;
- relatório da reprodução independente.

## Critérios de aprovação

| Critério | Meta |
|---|---:|
| cenários obrigatórios executados | 15/15 |
| violações críticas toleradas | 0 |
| casos sem proveniência | 0 |
| regressões não classificadas | 0 |
| hard gates aplicados antes da média | 100% |
| relatórios com justificativa e denominadores | 100% |
| segredos em logs | 0 |
| reprodução independente dos cálculos | concluída |

## Testes adversariais

- alterar severidade depois da execução;
- remover evidência de falha crítica;
- usar resultado do candidato como expected output;
- contaminar holdout;
- fazer grader aceitar texto sem evidência;
- esconder custo de retries;
- calcular p95 com amostra insuficiente;
- usar versões diferentes de dataset;
- descartar resultados ruins sem regra prévia;
- permitir média compensar violação crítica;
- alterar threshold após observar o resultado;
- reutilizar cache entre baseline e candidato.

## Troubleshooting

| Sintoma | Verificação segura |
|---|---|
| resultados variam muito | confira seed, temperatura, retries e dependências |
| baseline e candidato não são comparáveis | alinhe dataset, budgets, ambiente e política |
| grader discorda frequentemente | recalibre, inspecione casos e aplique revisão humana |
| p95 instável | aumente amostra e reporte intervalo e limitação |
| holdout foi consultado | invalide a rodada e crie nova partição protegida |

## Stop conditions

Pare imediatamente quando houver:

- schema incompatível;
- dataset ou grader set não versionado;
- baseline e candidato em condições diferentes;
- caso crítico sem hard gate;
- evidência adulterada;
- segredo em log;
- tentativa de reclassificar falha após resultado;
- holdout contaminado;
- denominador omitido em métrica decisória.

## Acessibilidade

- relatórios devem funcionar em texto puro;
- gráficos precisam de tabela equivalente;
- não use apenas cor para indicar regressão;
- tabelas devem ter cabeçalhos claros;
- comandos e resultados devem ser copiáveis;
- linguagem de aprovação e bloqueio deve ser explícita.

## Limpeza

Remova artefatos temporários com dados simulados quando não forem necessários, preserve apenas evidence bundles redigidos e registre hashes das versões avaliadas.

## Rubrica

| Nível | Evidência |
|---|---|
| insuficiente | média única, versões ausentes ou falha crítica compensada |
| funcional | comparação reproduzível com hard gates básicos |
| robusta | variância, trajetória, holdout e discordância são tratados |
| excelente | reprodução independente, cobertura por risco e decisão totalmente auditável |

## Limitações

Este laboratório não prova qualidade universal ou segurança absoluta. Ele produz evidência limitada ao dataset, graders, versões e condições executadas.

## Entrega Premium Elite

A entrega deve atender ao [gate transversal dos laboratórios](LABS_PREMIUM_ELITE_GATE.md) e permitir que outra pessoa explique exatamente por que o candidato foi aprovado, bloqueado ou enviado para revisão.