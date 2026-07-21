---
id: labs.index
title: Catálogo de laboratórios
lang: pt-BR
status: foundation
---

# Laboratórios

Laboratórios isolam uma hipótese e geram evidência reproduzível. Use dados sintéticos, ferramentas fake e credenciais sem privilégio.

| Lab | Módulo | Evidência |
|---|---|---|
| [LAB-000](LAB-000-repository-orientation.md) | 00 | relatório do validador + mapa de links |
| [LAB-101](LAB-101-agent-contract.md) | 01 | agent spec revisada |
| [LAB-201](LAB-201-context-selection-and-injection.md) | 02 | seleção de contexto avaliada contra corpus sintético |
| [LAB-301](LAB-301-safe-tool-boundary.md) | 03 | fronteira de ferramenta com policy gate e reconciliação |
| [LAB-401](LAB-401-stop-conditions.md) | 04 | matriz de terminação |
| [LAB-501](LAB-501-governed-memory.md) | 05 | memória governada com proveniência e expiração |
| [LAB-601](LAB-601-governed-multi-agent-coordination.md) | 06 | coordenação multiagente limitada e rastreável |
| [LAB-701](LAB-701-agent-evaluation-and-regression.md) | 07 | avaliação reproduzível e relatório de regressão |
| [LAB-801](LAB-801-agent-security-red-team.md) | 08 | red team controlado, containment e risco residual |
| [LAB-901](LAB-901-production-readiness.md) | 09 | evidência de rollout, operação e rollback |
| [LAB-1001](LAB-1001-agent-observability.md) | 10 | telemetria correlacionada, redaction e alertas |
| [LAB-1101](LAB-1101-idempotent-automation.md) | 11 | efeito único, reconciliação e compensação |

## Regra de unicidade

Cada número LAB identifica um único arquivo canônico. Variações e exercícios complementares devem ser incorporados ao laboratório principal ou receber identificador não conflitante.

Labs futuros descritos nos módulos devem ser marcados como planejados até existir um arquivo canônico e entrar no [roadmap](../ROADMAP.md). Todo novo lab usa [lab-template.md](../templates/lab-template.md).
