---
id: research.readiness-v4
title: Research Readiness V4 — após SDK Runtime Trial V1
lang: pt-BR
status: review
reviewed_at: 2026-08-26
---

# Research Readiness V4 — após SDK Runtime Trial V1

## O que mudou

O NEXUS saiu de Contract Trial puro e executou três boundaries oficiais reais:

- OpenAI Agents SDK 0.22.0 com `ScriptedModel`;
- Google ADK 2.8.0 com `Runner`/session real e `BaseLlm` offline;
- MCP Python SDK 2.1.1 com client/server in-process em 2026-07-28.

Isso eleva a evidência de **contrato** para **runtime conformance offline**.

## O que já é defensável

- versões oficiais realmente instaladas;
- runtime real realmente iniciado;
- tarefa determinística completada nos três;
- bounded failure observada nos três;
- protocol version 2026-07-28 observada no MCP;
- OpenAI tool pipeline exercitado com side effect NEXUS idempotente;
- evidência machine-readable + ambiente resolvido.

## O que NÃO é defensável

- OpenAI versus Google em qualidade;
- qualquer ranking de latência;
- custo/token efficiency;
- segurança intrínseca contra prompt injection;
- superioridade de HITL/A2A;
- segurança MCP remota;
- production-grade.

## Readiness por domínio

| Domínio | Estado |
|---|---|
| Contract parity | ALTO |
| Offline SDK runtime conformance | ALTO para os cenários executados |
| OpenAI side-effect integration | MÉDIO-ALTO, sintético/controlado |
| Google A2A/HITL | NÃO EXECUTADO |
| MCP remote/auth/MRTR | NÃO EXECUTADO |
| Provider/model comparison | NÃO EXECUTADO |
| Supply-chain reproducibility | MÉDIO-ALTO; falta hash lock |
| Statistical plan | NÃO NECESSÁRIO para smoke; necessário antes de provider/model |
| Adversarial model evaluation | NÃO EXECUTADO |
| Scientific publication readiness | PILOTO/MÉTODO, não conclusão comparativa |

## Próximo desenho científico

O próximo estudo não deve simplesmente adicionar mais frameworks. Deve fechar as assimetrias:

1. cenário side-effect/tool equivalente no ADK e MCP host;
2. A2A/HITL pause/resume no ADK;
3. MCP HTTP/auth/MRTR adversarial lab;
4. OTel/redaction por runtime;
5. lockfiles transitivos com hashes;
6. somente depois Provider/Model Trial controlado.

## Maturity

**L3 — Reproducible**, ampliado para SDK runtime offline.

O salto para L4 depende de segurança executada nas boundaries remotas e supply chain mais forte.
