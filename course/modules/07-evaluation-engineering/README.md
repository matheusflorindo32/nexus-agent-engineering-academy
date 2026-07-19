---
id: course.module.07-evaluation-engineering
title: 07 — Evaluation Engineering
lang: pt-BR
status: review
version: 0.1.0
estimated_time: 14h
prerequisites: [course.module.06-multi-agent-systems]
learning_outcomes:
  - desenhar sistemas de avaliação reproduzíveis para agentes
  - construir datasets com cobertura, proveniência e versionamento
  - combinar graders determinísticos, heurísticos e humanos
  - detectar regressões de qualidade, segurança, custo e latência
---

# 07 — Evaluation Engineering

> [!IMPORTANT]
> Um agente sem avaliação contínua é apenas uma demonstração plausível. Engenharia começa quando comportamento, custo, segurança e regressão podem ser medidos e explicados.

## Objetivos

- Transformar requisitos em critérios observáveis e mensuráveis.
- Construir datasets versionados, representativos e adversariais.
- Implementar graders determinísticos, heurísticos, por modelo e humanos com limites explícitos.
- Comparar versões por baseline, regressão e significância operacional.
- Separar avaliação offline, shadow, canary e produção.
- Produzir relatórios auditáveis por caso, dimensão e release.

## Pré-requisitos

[Módulo 06](../06-multi-agent-systems/README.md); JSON, testes, contratos, métricas básicas e controle de versões.

## O problema real

Avaliar agentes é difícil porque a saída pode ser linguisticamente diferente e ainda correta, ou parecer correta e violar requisitos críticos. Métricas únicas escondem falhas importantes.

A NEXUS exige avaliação multidimensional:

| Dimensão | Pergunta |
|---|---|
| Correção | o resultado satisfaz o objetivo verificável? |
| Groundedness | afirmações estão apoiadas nas evidências permitidas? |
| Segurança | políticas, escopos e limites foram respeitados? |
| Processo | ferramentas, handoffs e estados seguiram o contrato? |
| Robustez | o sistema resiste a ruído, ambiguidade e ataques? |
| Eficiência | custo, latência e chamadas permanecem dentro do budget? |
| Experiência | a resposta é útil, clara e adequada ao usuário? |

Nenhuma média global pode compensar falha em um critério bloqueante.

## Contrato de caso de avaliação

```json
{
  "case_id": "eval-001",
  "dataset_version": "2026.07.1",
  "input": {"request": "..."},
  "expected": {
    "required_facts": ["..."],
    "forbidden_actions": ["write_external"],
    "terminal_state": "complete"
  },
  "tags": ["core", "security"],
  "severity": "critical",
  "source_refs": ["policy:v3"],
  "grader_policy": "grader-set:v2"
}
```

Cada caso deve possuir identidade estável, origem, propósito, severidade e política de avaliação.

## Dataset Engineering

Um dataset de avaliação não é uma coleção aleatória de prompts. Ele precisa cobrir:

- caminho feliz;
- limites de escopo;
- entradas ambíguas;
- dados incompletos;
- conflitos entre fontes;
- prompt injection;
- falhas de ferramenta;
- latência e timeout;
- retomada e idempotência;
- casos raros de alto impacto.

### Partições mínimas

| Partição | Uso |
|---|---|
| `development` | iteração rápida; não usada como prova final |
| `validation` | ajuste de políticas e thresholds |
| `regression` | histórico de falhas reais e corrigidas |
| `holdout` | comparação final sem contaminação |
| `adversarial` | ataques, abuso e condições extremas |

Casos originados de incidentes devem entrar na suíte de regressão com referência ao incidente e correção esperada.

## Tipos de graders

### Determinístico

Adequado para:

- schema;
- igualdade exata;
- presença ou ausência de campos;
- terminal state;
- número de chamadas;
- políticas e permissões;
- hashes, IDs e limites.

É preferido sempre que o requisito puder ser formalizado.

### Heurístico

Usa regras explicáveis como cobertura de termos, padrões, distância ou consistência interna. Deve declarar falsos positivos e falsos negativos conhecidos.

### Model-based grader

Útil para critérios semânticos, mas não é verdade absoluta. Requer:

- prompt e versão fixados;
- rubrica explícita;
- saída estruturada;
- calibração contra humanos;
- teste de estabilidade;
- isolamento de dados sensíveis;
- desempate quando houver baixa confiança.

### Avaliação humana

Necessária para experiência, adequação contextual e calibração. Avaliadores precisam de rubrica, exemplos, cegamento quando possível e registro de discordância.

## Hierarquia de decisão

```text
hard gates → critérios críticos → dimensões ponderadas → custo/latência → decisão de release
```

Exemplo:

```yaml
hard_gates:
  policy_violations: 0
  cross_tenant_leaks: 0
  duplicate_effects: 0
  critical_case_pass_rate: 1.0
quality_thresholds:
  overall_pass_rate: 0.95
  groundedness: 0.92
  task_success: 0.94
operational_thresholds:
  p95_latency_ms: 2500
  mean_tool_calls: 4.0
  cost_per_success_usd: 0.08
```

## Métricas essenciais

- `case_pass_rate`;
- `critical_pass_rate`;
- `task_success_rate`;
- `groundedness_rate`;
- `policy_violation_rate`;
- `tool_error_rate`;
- `handoff_failure_rate`;
- `mean_cost_per_case`;
- `cost_per_success`;
- `p50/p95/p99 latency`;
- `retry_rate`;
- `abstention_quality`;
- `grader_disagreement_rate`.

Sempre apresente denominador, intervalo temporal e versão do dataset.

## Baseline e regressão

Cada candidato deve ser comparado contra um baseline imutável. Uma regressão pode existir mesmo quando a média melhora.

Bloqueie release quando ocorrer:

- qualquer falha nova em caso crítico;
- violação de hard gate;
- queda acima do tolerance budget por dimensão;
- aumento de custo ou latência sem ganho proporcional aprovado;
- instabilidade significativa entre execuções repetidas;
- aumento de discordância dos graders.

## Repetição e variância

Sistemas probabilísticos devem executar múltiplas repetições por caso quando a variância for material. Registre seed quando suportada e, quando não for, registre modelo, parâmetros, horário, região e versão do adapter.

Métricas recomendadas:

- média e mediana;
- desvio e amplitude;
- pior caso;
- taxa de sucesso em `n` tentativas;
- consistência entre execuções.

## Avaliação de trajetória

A resposta final sozinha é insuficiente. Avalie:

- plano gerado;
- seleção de contexto;
- ferramentas escolhidas;
- argumentos;
- retries;
- handoffs;
- aprovações;
- efeitos externos;
- razão terminal.

Trajetórias incorretas que ocasionalmente produzem resposta correta devem ser tratadas como risco.

## Contaminação e leakage

Separe dados de desenvolvimento e holdout. Evite publicar integralmente casos reservados. Registre exposição de casos a prompts, modelos ou pessoas que ajustam o sistema.

Sinais de contaminação:

- respostas memorizadas;
- desempenho anormalmente alto em casos públicos;
- queda severa em variantes semanticamente equivalentes;
- uso de identificadores exclusivos do dataset.

## Offline, shadow, canary e produção

| Estágio | Objetivo |
|---|---|
| Offline | segurança e regressão sem efeitos reais |
| Shadow | comparar candidato com tráfego real sem controlar resultado |
| Canary | exposição limitada com rollback rápido |
| Produção | SLOs, alertas, incidentes e coleta de novos casos |

Passar em offline é necessário, mas não suficiente para produção.

## Relatório de avaliação

O relatório mínimo inclui:

```json
{
  "run_id": "eval-run-042",
  "candidate": "agent:v1.4.0",
  "baseline": "agent:v1.3.2",
  "dataset": "nexus-eval:2026.07.1",
  "total_cases": 120,
  "passed": 116,
  "critical_failures": 0,
  "regressions": 2,
  "hard_gates_passed": true,
  "release_decision": "blocked",
  "reason": "groundedness regression above tolerance"
}
```

Resultados por caso devem preservar evidências e diferenças sem registrar segredos.

## Implementação de referência

Execute:

```bash
python examples/evaluation_harness.py --self-test
```

A implementação demonstra:

- dataset versionado;
- graders determinísticos e heurísticos;
- hard gates;
- baseline versus candidato;
- classificação de regressões;
- custo e latência;
- relatório JSON;
- 12 cenários reproduzíveis sem rede.

## Laboratório

- [LAB-701](../../../labs/LAB-701-agent-evaluation-and-regression.md) — construir uma suíte de avaliação com release gate.

## Projeto

Construir um evaluation harness que:

1. carregue casos versionados;
2. valide schema e proveniência;
3. execute baseline e candidato;
4. aplique graders independentes;
5. compute métricas por dimensão e severidade;
6. identifique regressões e melhorias;
7. aplique hard gates e thresholds;
8. produza relatório legível por máquina e humano;
9. gere evidência de repetição e variância;
10. bloqueie release quando necessário.

## Quiz

1. Por que uma média global pode esconder uma falha grave?
2. Quando um grader determinístico deve ser preferido?
3. Por que model-based graders precisam de calibração?
4. Qual a função de um holdout?
5. Por que avaliar a trajetória além da resposta final?

<details>
<summary>Gabarito comentado</summary>

1. Porque ganhos em casos fáceis podem compensar numericamente violações críticas.
2. Sempre que o requisito puder ser formalizado sem julgamento semântico subjetivo.
3. Porque também são probabilísticos, enviesados e sensíveis ao prompt.
4. Medir generalização sem contaminação pelo processo de ajuste.
5. Porque uma resposta correta pode ter sido obtida por processo inseguro, caro ou não reproduzível.

</details>

## Checklist

- [ ] Casos possuem IDs, versões, severidade, tags e proveniência.
- [ ] Há partições development, regression, holdout e adversarial.
- [ ] Hard gates não podem ser compensados por médias.
- [ ] Graders são versionados e possuem limitações documentadas.
- [ ] Baseline e candidato são executados nas mesmas condições.
- [ ] Regressões são avaliadas por caso e dimensão.
- [ ] Custo, latência, chamadas e falhas operacionais são medidos.
- [ ] Variância é registrada quando relevante.
- [ ] Trajetória e efeitos são avaliados.
- [ ] Relatório contém decisão e justificativa auditável.

## Critérios de excelência

| Dimensão | Padrão Premium Elite |
|---|---|
| Cobertura | requisitos, riscos e incidentes mapeados para casos |
| Reprodutibilidade | dataset, graders, parâmetros e versões fixados |
| Segurança | zero violação crítica tolerada |
| Comparabilidade | baseline e candidato sob condições equivalentes |
| Diagnóstico | falhas localizadas por caso, dimensão e trajetória |
| Governança | release gate explícito, justificável e revisável |

## Referências

- NIST — AI Risk Management Framework e Generative AI Profile.
- Google — Rules of Machine Learning: Testing and Monitoring.
- Microsoft — Responsible AI Standard e avaliação de aplicações generativas.
- OpenAI — documentação oficial de evals e graders.
- ISO/IEC 25010 — modelos de qualidade de sistemas e software.

> [!WARNING]
> Scores automáticos são evidências, não decisões finais universais. Em domínios de alto impacto, revisão humana e validação específica continuam obrigatórias.

## Próximo passo

Conclua o LAB-701 e estabeleça um release gate reproduzível antes de avançar para segurança e operação em produção.
