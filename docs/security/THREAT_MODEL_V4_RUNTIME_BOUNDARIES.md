---
id: security.threat-model-v4-runtime-boundaries
title: Threat Model V4 — SDK runtime boundaries
lang: pt-BR
status: review
reviewed_at: 2026-08-26
---

# Threat Model V4 — SDK runtime boundaries

Este documento estende o Threat Model V3 após a primeira execução de runtimes oficiais.

## Boundaries executados

| Boundary | Executado | Evidência | Residual |
|---|---|---|---|
| NEXUS → OpenAI Agents SDK | sim | Runner + ScriptedModel + tool pipeline | provider/model real não testado |
| NEXUS → Google ADK | sim | Runner + InMemorySessionService + BaseLlm offline | A2A/HITL/tool side effects pendentes |
| NEXUS host → MCP Python SDK | sim | MCPServer + Client in-process, 2026-07-28 | HTTP/OAuth/DNS/MRTR pendentes |
| NEXUS → Microsoft Agent Framework | não | MONITORING | contract parity primeiro |

## Novas ameaças confirmadas pelo desenho

### Resolver de dependências transitivas
**Ameaça:** top-level pin reproduz SDK, mas não garante grafo transitivo imutável.

**Controle atual:** job isolado, `pip check`, `pip freeze`, artifact.

**Residual:** médio. Próximo controle: constraints/lock com hashes e provenance attestation.

### Confusão de SHA em pull_request
**Ameaça:** merge ref do GitHub ser confundido com head da branch.

**Controle:** registrar `commit_sha` e `workflow_sha` separadamente.

**Residual:** baixo.

### Métrica host confundida com propriedade de framework
**Ameaça:** VAR/DSER/CTVR do NEXUS ser apresentada como capacidade nativa do SDK.

**Controle:** `test_boundary`, `claims`, null/NOT_EXECUTED e revisão metodológica.

**Residual:** baixo se consumers preservarem metadata.

## Ameaças ainda não testadas

### OpenAI
- provider timeout/network;
- replay/session persistence com provider real;
- guardrail-blocked sensitive tool output no fluxo completo;
- MCP remoto/tool poisoning;
- tracing e redaction com spans reais.

### Google ADK
- A2A peer identity;
- HITL pause/resume;
- parallel tool side effects;
- session restore;
- remote MCP;
- Model Armor effectiveness;
- experimental telemetry leakage/redaction.

### MCP
- HTTP transport;
- DNS rebinding;
- OAuth issuer/audience/resource;
- server discovery metadata;
- MRTR interruption;
- cancellation across network;
- credential passthrough;
- tool poisoning remoto.

## Regras V4

1. Runtime real sem provider real deve ser rotulado `SDK_RUNTIME_OFFLINE`.
2. Falha ausente/não equivalente deve ser `NOT_EXECUTED`, nunca zero.
3. `runtime_duration_ms` offline não pode ser usado para ranking.
4. Side effect crítico exige receipt externa ao modelo.
5. Dependência major/minor nova repassa pelo Upgrade Gate.
6. Conteúdo MCP remoto continua T6.
7. Provider/model trial exige consentimento explícito para custo/credencial.
