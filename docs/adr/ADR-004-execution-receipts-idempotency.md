---
id: adr.004.execution-receipts-idempotency
title: ADR-004 — Execution Receipts e Idempotência
lang: pt-BR
status: review
---

# ADR-004 — Execution Receipts e Idempotência

## Status

Proposto para revisão humana; efetivo após merge explícito.

## Contexto

Aprovação humana, chamada de tool e resposta textual do agente são eventos distintos. Falhas de transporte, retries e resumes podem tornar ambíguo se um side effect aconteceu.

## Decisão

Toda ação externa relevante deve usar `operation_id` e distinguir:

`REQUESTED → APPROVED → EXECUTED → VERIFIED`.

Ferramentas com side effects devem produzir um `ExecutionReceipt` persistível contendo, no mínimo, operação, tool, principal, timestamps, status, alvo/recurso verificável, hash de resultado quando aplicável e retry count.

Retries de side effects devem consultar receipt/reconciliação antes de reexecutar.

## Consequências

- a narrativa do LLM deixa de ser prova de execução;
- approval precisa ser scoped para operação/principal;
- observabilidade passa a correlacionar `run_id` e `operation_id`;
- testes podem medir Verified Action Rate e Duplicate Side Effect Rate.

## Alternativas rejeitadas

### Confiar no status textual da tool/modelo

Rejeitada porque não resolve resultado ambíguo após falha de transporte.

### Retry cego

Rejeitado por risco de efeitos duplicados.

## Critérios de aceite

- reference runtime com `ActionLedger`/receipt;
- teste de duplicate execution;
- teste de scoped HITL;
- teste de verification separado de execution;
- adapters reais documentam como obtêm evidência externa de execução.

## Risco residual

O ledger de referência é in-memory e não fornece exactly-once distribuído. Produção precisa de armazenamento durável/transacional ou mecanismo equivalente do sistema-alvo.