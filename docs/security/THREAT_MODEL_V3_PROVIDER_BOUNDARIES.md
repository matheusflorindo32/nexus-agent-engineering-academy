---
id: security.threat-model-v3-provider-boundaries
title: Threat Model V3 — fronteiras de providers e protocolo
lang: pt-BR
status: review
reviewed_at: 2026-08-26
---

# Threat Model V3 — fronteiras de providers e protocolo

Este documento é um delta do Threat Model V2 para o milestone Provider Adapters V3.

## Novas fronteiras

| Fronteira | Ameaça principal | Impacto | Controle V3 | Risco residual |
|---|---|---|---|---|
| NEXUS → OpenAI Agents SDK | mudança de semântica em approvals/state/replay entre releases | ação incorreta ou estado inconsistente | version pin + upgrade gate + contract oracle | médio até runtime trial |
| NEXUS → Google ADK | A2A/HITL resume, parallel tool state, session correctness | approval sem execução verificável, duplicação, state contamination | receipt externo + typed resume + regression suite | médio/alto até reprodução real |
| NEXUS host → MCP | metadata/tool output hostil, version mismatch, auth mal configurada | prompt injection, exfiltração, confused deputy | T6 default + version negotiation + allowlist + no passthrough | médio/alto até MCP lab real |
| Provider trace → observability | payload sensível em spans/logs | vazamento de segredo/dados | redaction antes de export + schema allowlist | médio |
| Dependency registry → adapter | upgrade malicioso/incompatível | supply-chain compromise | lock/pin + provenance + dependency review | médio |
| Benchmark harness → conclusão | benchmark de contrato interpretado como performance real | claim científico falso | `claims_scope` machine-readable + docs/CI limitations | baixo |

## Regras de segurança

1. Nenhum adapter real herda confiança do nome do fornecedor.
2. Output de modelo/tool/MCP permanece dado não confiável até validação.
3. Approval textual não prova execução.
4. SDK state não substitui receipt externo para side effect crítico.
5. Upgrade minor/major de framework agentic exige regression benchmark antes de adoção.
6. Falha ambígua de transporte exige reconciliation antes de retry não idempotente.
7. Provider tracing não pode persistir secrets por conveniência de debug.

## Cenários prioritários para Runtime Trial

- OpenAI: model timeout, interruption/replay, guardrail-blocked tool output, MCP/tool result injection.
- Google ADK: A2A HITL pause/resume, parallel tool calls com approval, session restore, duplicate retry.
- MCP: version negotiation 2026-07-28, malicious tool description/result, auth audience/resource mismatch, MRTR interruption.

## Estado

Os controles de contrato são executáveis em CI. Os riscos de runtime permanecem `POTENTIALLY_APPLICABLE` ou `MONITORING` até execução com SDK/protocolo real.
