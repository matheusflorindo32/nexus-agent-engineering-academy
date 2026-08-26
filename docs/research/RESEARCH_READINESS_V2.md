---
id: research.readiness-v2
title: Research Readiness V2
lang: pt-BR
status: review
reviewed_at: 2026-08-25
---

# Research Readiness V2

## Pergunta metodológica

O NEXUS está pronto para produzir comparações defensáveis entre frameworks/arquiteturas de agentes?

**Resposta atual:** parcialmente. A fundação já permite desenhar estudos, mas ainda faltam adapters equivalentes, ambientes versionados e resultados executados para alegar comparações científicas.

## Hipóteses prioritárias

### H1 — Reliability

Arquiteturas com timeout, terminal-error propagation, bounded retry e reconciliation terão maior `Recovery Success Rate` e menor taxa de runs travados que arquiteturas sem esses controles.

### H2 — Verified actions

Separar `APPROVED`, `EXECUTED` e `VERIFIED` com receipts reduzirá discrepâncias entre ações declaradas e ações realmente concluídas.

### H3 — Skill lifecycle

Versionamento imutável + staging + hash + promoção atômica reduzirá falhas transitórias e inconsistência de loader durante atualização concorrente de Skills.

### H4 — Context trust

Taxonomia explícita de confiança e policy gate fora do modelo reduzirão violações em cenários de indirect prompt injection/MCP tool poisoning.

## Métricas V2

- Task Success Rate;
- Correctness;
- Latency;
- Token usage / estimated cost quando aplicável;
- Tool calls;
- Error/retry rate;
- State integrity;
- Verified Action Rate (VAR);
- Recovery Success Rate (RSR);
- Duplicate Side Effect Rate (DSER);
- Context Trust Violation Rate (CTVR).

## Requisitos de desenho experimental

1. Mesma tarefa e dataset para frameworks comparados.
2. Versões e configurações registradas.
3. Prompt/Skill versionados.
4. Seeds quando aplicáveis e, quando não aplicáveis, repetição suficiente para variabilidade estocástica.
5. Definição prévia de sucesso/falha.
6. Separação entre benchmark determinístico do control-plane e benchmark dependente de modelo.
7. Logs/traces sem secrets, com correlação por `run_id` e `operation_id`.
8. Resultados em formato machine-readable.
9. Falhas e exclusões reportadas, não descartadas silenciosamente.
10. Não inferir causalidade de comparação observacional simples.

## Maturidade por componente

| Componente | Readiness |
|---|---|
| Contratos conceituais | ALTO |
| Segurança e threat modeling | MÉDIO-ALTO, V2 em revisão |
| Runtime determinístico de hardening | MÉDIO |
| Testes unitários de hardening | MÉDIO, aguardando CI |
| Adapters reais comparáveis | BAIXO/PARCIAL |
| Dataset benchmark multi-framework | BAIXO |
| Protocolo preregistrável | PARCIAL |
| Statistical analysis plan | NÃO IMPLEMENTADO |
| Artefatos reproduzíveis/containerizados | PARCIAL |
| Relatório final científico | NÃO IMPLEMENTADO |

## Próximo gate científico

Antes de qualquer claim do tipo “framework A é mais seguro/confiável que B”, criar um protocolo versionado com tarefas, ameaças, métricas, número de repetições, critérios de exclusão, análise e limitações.

## Classificação

**Research-ready para desenho/piloto; não research-ready para conclusão comparativa pública.**