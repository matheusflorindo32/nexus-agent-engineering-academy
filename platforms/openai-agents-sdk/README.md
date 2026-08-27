---
id: platform.openai-agents-sdk
title: Adapter experimental — OpenAI Agents SDK
lang: pt-BR
status: review
verified: 2026-08-26
---

# Adapter experimental — OpenAI Agents SDK

Fonte primária: documentação e releases oficiais de `openai/openai-agents-python`.

- Versão estável verificada: `0.22.0` (2026-08-19).
- Status NEXUS: `trial-runtime-offline`.
- Execução real do SDK: **sim**, com `Runner`/tool pipeline reais e `ScriptedModel` oficial, sem API/provider externo.

## Capacidades verificadas

| Conceito NEXUS | Suporte upstream | Regra NEXUS |
|---|---|---|
| Agents + instructions | suportado | instrução não substitui policy gate |
| Tools | suportado | schema, escopo, idempotência e receipts |
| Handoffs | suportado | trace e estado precisam ser reconciliáveis |
| Guardrails | suportado | camada defensiva, não autoridade única |
| Tracing | suportado | redaction antes de persistência/export |
| Sessions/RunState | suportado | interruption/replay precisam de teste |
| MCP | suportado | conteúdo remoto é T6 por padrão |

## Evidência recente

A release 0.22.0 registra hardening de runtime e data isolation, incluindo redaction de terminal tool output bloqueado por output guardrails, erro explícito para Responses `failed`/`incomplete`, isolamento de usage entre checkpoints e expansão de handoffs em grafos. A 0.21.1 registra model-call timeouts, networking opcionalmente desabilitado em sandbox e correções de approval decisions e cleanup após falhas.

## Classificação NEXUS

- hardening 0.22.0: `MONITORING`;
- timeout/cleanup: `POTENTIALLY_APPLICABLE` ao futuro adapter real;
- vulnerabilidade NEXUS reproduzida: **nenhuma alegada**.

## Gate para adapter executável

Antes de chamar este adapter de `verified`, demonstrar com SDK pinado:

1. timeout/cancellation bounded;
2. approval scoped por `operation_id`, principal, ação e alvo;
3. `APPROVED != EXECUTED != VERIFIED`;
4. retry de side effect sem duplicação;
5. tracing/redaction sem segredos;
6. guardrail state/replay testado;
7. MCP/tool outputs tratados pelo Context Trust Model.

O benchmark V3 atual mede apenas o **contrato NEXUS determinístico**, não desempenho ou segurança do runtime OpenAI real.

## Runtime Trial V1

O SDK 0.22.0 foi instalado e executado em CI. O cenário determinístico completou o marcador, propagou falha injetada de forma bounded e atravessou duas tool calls idênticas com uma única execução do side effect NEXUS. VAR=1.0 e DSER=0.0 valem para a combinação **SDK runtime + controles NEXUS**, não como garantia nativa do SDK.
