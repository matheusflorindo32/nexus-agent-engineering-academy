---
id: governance.next-milestone-v2
title: Próximo Milestone — Hardening V2
lang: pt-BR
status: review
reviewed_at: 2026-08-25
---

# Próximo Milestone — Hardening V2

## Objetivo

Converter os controles de referência em evidência executável e preparar adapters reais sem introduzir lock-in ou claims não comprovados.

## Ordem

### Gate 1 — CI e regressão

- executar validator;
- executar `unittest discover`;
- executar `compileall`;
- executar todos os self-tests;
- corrigir qualquer falha da branch.

### Gate 2 — ADRs

Registrar decisões sobre:

- Context Trust Model;
- Execution Receipts + idempotency;
- Atomic Skill Updates;
- Framework Upgrade Gate.

### Gate 3 — benchmark schema

Criar schema machine-readable para:

- VAR;
- RSR;
- DSER;
- CTVR;
- latency/errors/retries.

### Gate 4 — Skills lifecycle MVP

Criar apenas o mínimo:

- manifest/registry simples;
- staging;
- validation;
- hash;
- status;
- atomic promotion;
- rollback.

Não criar serviço/DB se arquivo estruturado atender ao experimento.

### Gate 5 — adapters controlados

Ordem recomendada:

1. OpenAI Agents SDK — tool lifecycle/tracing;
2. Google ADK Python — HITL/A2A state integrity;
3. MCP — untrusted metadata/tool output;
4. Go/TypeScript apenas quando o experimento exigir.

### Gate 6 — chaos lab

Simular timeout, disconnect, partial result, duplicate result, state corruption, MCP unavailable e credential expiry.

### Gate 7 — auditoria independente

Arquitetura, AppSec, Agent Security, MCP Security, Supply Chain, Reliability, Test Engineering e Reproducibility.

## Definition of Done

O milestone termina quando:

- CI está verde;
- testes novos possuem evidência;
- nenhuma descoberta upstream é apresentada como vulnerabilidade local sem reprodução;
- actions críticas usam `operation_id` e receipt no reference layer;
- trust model e Skill lifecycle têm ADR;
- benchmark schema está versionado;
- riscos residuais estão explícitos;
- PR está aberto, sem auto-merge.