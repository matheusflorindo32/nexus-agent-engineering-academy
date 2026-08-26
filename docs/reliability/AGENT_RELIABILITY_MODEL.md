---
id: reliability.agent-model
title: Agent Reliability Model
lang: pt-BR
status: review
reviewed_at: 2026-08-25
---

# Agent Reliability Model

## Objetivo

Tratar agentes como sistemas distribuídos probabilísticos, não como simples chamadas de API.

## Invariantes

1. Toda espera remota possui timeout.
2. Toda operação cancelável expõe cancelamento observável.
3. Retry requer budget, backoff e classificação de idempotência.
4. Falha terminal deve ser propagada a consumidores presentes e futuros.
5. Side effect ambíguo não deve ser repetido sem reconciliação.
6. Resume exige checkpoint compatível e estado validado.
7. Falha parcial deve ser representada explicitamente.
8. O sistema deve preferir falha segura a conclusão fabricada.

## Classes de falha

- model/provider;
- transport/stream;
- tool;
- MCP;
- storage/memory;
- orchestration/handoff;
- approval/HITL;
- state/checkpoint;
- dependency/configuration;
- policy/security.

## Política de retry

| Classe | Retry automático | Requisito |
|---|---|---|
| timeout read-only | sim, limitado | backoff + budget |
| transport failure antes de side effect | sim, limitado | prova de não execução |
| resultado de side effect ambíguo | não imediatamente | reconcile por `operation_id`/receipt |
| auth/permission | não | corrigir identidade/escopo |
| validation/schema | não | corrigir input/contrato |
| rate limit | sim | `Retry-After`/backoff |
| policy denial | não | decisão humana/política |

## State machine de reliability

```text
RUNNING
├─ success → COMPLETED
├─ cancel → CANCELLED
├─ transient failure → RETRY_WAIT → RUNNING
├─ ambiguous side effect → RECONCILING → RUNNING|FAILED_SAFE
├─ recoverable crash → CHECKPOINT_RESTORE → RUNNING
└─ terminal/policy failure → FAILED_SAFE
```

## Execution receipts

Ferramentas com side effect devem produzir receipt persistível e consultável. `tool.executed` sem evidência externa não é suficiente para `tool.verified`.

## Métricas

### Verified Action Rate (VAR)

`ações verificadas / ações declaradas concluídas`

### Recovery Success Rate (RSR)

`execuções recuperadas corretamente / tentativas de recovery`

### Duplicate Side Effect Rate (DSER)

`side effects duplicados / side effects totais`

Meta para operações críticas: `0` duplicações observadas.

### Context Trust Violation Rate (CTVR)

`violações de fronteira de confiança / casos adversariais executados`

## Chaos/failure test matrix

- API timeout;
- model timeout;
- stream interrompido;
- consumer cancelado;
- MCP indisponível;
- storage indisponível;
- state corrompido;
- tool result malformado;
- resposta duplicada;
- rate limit;
- credential expiry;
- context overflow;
- approval expirado;
- handoff parcial.

## Observabilidade mínima

Eventos canônicos:

- `run.started`
- `agent.started`
- `tool.requested`
- `tool.approval_requested`
- `tool.approved`
- `tool.executed`
- `tool.failed`
- `tool.verified`
- `handoff.started`
- `handoff.completed`
- `recovery.started`
- `recovery.completed`
- `run.completed`
- `run.failed`

Cada evento deve possuir `run_id`, timestamp, componente, status e correlação; side effects devem também carregar `operation_id`.

## Gate de maturidade

O modelo permanece `review` até que testes de timeout, cancelamento, retry, side-effect reconciliation e resume sejam executados em CI.