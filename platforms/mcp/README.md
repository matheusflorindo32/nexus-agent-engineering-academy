---
id: platform.mcp-2026-07-28
title: Adapter experimental — MCP 2026-07-28
lang: pt-BR
status: review
verified: 2026-08-26
---

# Adapter experimental — MCP 2026-07-28

Fonte primária: especificação e release oficiais de `modelcontextprotocol/modelcontextprotocol`.

- Revisão estável verificada: `2026-07-28`.
- Status NEXUS: `trial-runtime-in-process`.
- Execução real de SDK/servidor MCP: **sim**, Python SDK 2.1.1 com `MCPServer` + `Client` in-process.

## Mudanças arquiteturais verificadas

A revisão 2026-07-28 torna o core do protocolo stateless, remove handshake/sessões de protocolo, move versão e capacidades para `_meta` por request, introduz header-based routing, Multi Round-Trip Requests, cache hints/list ordering, extensões formais e hardening de autorização.

## Interpretação NEXUS

MCP é protocolo de contexto/ferramentas, não substitui o host/orchestrator. Portanto, HITL, policy gates, receipts, tracing e autorização de efeitos continuam responsabilidade do host quando não forem fornecidos por uma extensão/implementação específica.

Conteúdo vindo de servidor MCP, incluindo tool metadata e resultados, entra como `T6 — external/third-party content` até promoção explícita por política determinística.

## Classificação

- mudança stateless/compatibilidade: `MONITORING`;
- trust boundary de conteúdo remoto: `MITIGATED` no reference layer por T0–T7;
- comportamento de SDK real 2026-07-28: `POTENTIALLY_APPLICABLE` até execução pinada;
- vulnerabilidade NEXUS reproduzida: **nenhuma alegada**.

## Gate para adapter executável

1. version negotiation/opt-in explícito testado;
2. servidor e versão registrados por provenance;
3. tools allowlisted por schema e efeito;
4. metadata/resultados não elevam trust level;
5. auth com issuer/audience/resource validation quando aplicável;
6. sem credential passthrough;
7. timeout/cancel/retry bounded;
8. MRTR e state handles testados sem sessão implícita;
9. traces e logs sem credenciais.

O benchmark V3 atual não mede latência, disponibilidade ou segurança de implementações MCP reais.

## Runtime Trial V1

O Python SDK 2.1.1 foi instalado e executado em CI. O client negociou `2026-07-28`, chamou uma tool de marcador e observou uma `ToolError` determinística sem hang. HTTP, OAuth, DNS, MRTR e server discovery remoto permanecem NOT_EXECUTED.
