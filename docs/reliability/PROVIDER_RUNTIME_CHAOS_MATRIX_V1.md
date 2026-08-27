---
id: reliability.provider-runtime-chaos-v1
title: Provider Runtime Trial V1 — failure injection e chaos matrix
lang: pt-BR
status: review
reviewed_at: 2026-08-26
---

# Provider Runtime Trial V1 — failure injection e chaos matrix

## Escopo executado

O V1 executa **failure-injection smoke**, não chaos engineering completo de infraestrutura.

| Adapter | Falha injetada | Boundary | Resultado esperado |
|---|---|---|---|
| OpenAI Agents SDK 0.22.0 | erro determinístico do `ScriptedModel` | model boundary do SDK | exceção observável antes do timeout |
| Google ADK 2.8.0 | `RuntimeError` do `BaseLlm` offline | model boundary do ADK | exceção observável antes do timeout |
| MCP 2.1.1 | `ToolError` da tool real | client/server in-process | `is_error` antes do timeout |

Esses cenários alimentam RSR no escopo executado.

## Não executado neste V1

- packet loss;
- HTTP disconnect;
- DNS failure;
- OAuth expiry;
- provider rate limit;
- provider cancellation;
- process crash;
- storage outage;
- corrupted persisted session;
- A2A peer loss;
- MRTR interruption;
- remote MCP restart.

## Regra metodológica

Um cenário não executado não recebe score zero nem score de sucesso. Ele recebe `NOT_EXECUTED`.

## Próximo nível

Runtime Security Convergence V1.1 deverá transformar essa smoke matrix em chaos suite com falhas de transporte, estado, auth e side effects equivalentes.
