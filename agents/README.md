---
id: agents.index
title: Engenharia de agentes
lang: pt-BR
status: foundation
---

# Engenharia de agentes

Um agente NEXUS é definido por objetivo, política, estado, ferramentas, loop, budgets, observabilidade e critérios de
parada. “Persona” é opcional; controles operacionais não são.

## Contrato mínimo

```yaml
id: research-agent
objective: produzir síntese rastreável
inputs: [question, approved_sources]
tools: [search_read_only]
policy: no_external_writes
budgets: {steps: 12, minutes: 10}
approval_required: [publish]
stop_on: [objective_met, no_progress, budget_exhausted, policy_violation]
outputs: [answer, evidence, uncertainty]
```

## Padrões

- **Single agent:** escolha padrão até a decomposição demonstrar ganho.
- **Router + specialists:** roteamento explícito por capacidade.
- **Planner–executor:** plano separado da execução; útil quando revisão agrega controle.
- **Generator–critic:** crítica independente com rubrica, sem loop ilimitado.
- **Human-in-the-loop:** estado de espera persistível, decisão com escopo e expiração.

Multiagentes aumentam custo, latência e superfície de falha. Exija hipótese, métrica e baseline single-agent antes de
adotá-los. Veja [loops](../loops/README.md), [segurança](../docs/security/index.md) e o
[template de agent spec](../templates/agent-spec.md).

