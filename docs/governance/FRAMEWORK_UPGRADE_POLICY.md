---
id: governance.framework-upgrade-policy
title: Framework Upgrade Policy
lang: pt-BR
status: review
reviewed_at: 2026-08-25
---

# Framework Upgrade Policy

## Objetivo

Evitar que atualizações de frameworks agentic alterem silenciosamente semântica de tools, state, HITL, tracing ou segurança.

## Gate obrigatório

```text
NEW VERSION DETECTED
→ RELEASE NOTES REVIEW
→ SECURITY/ISSUE REVIEW
→ LICENSE/DEPENDENCY REVIEW
→ SANDBOX BRANCH
→ REGRESSION TESTS
→ AGENT BENCHMARKS
→ SECURITY BENCHMARKS
→ COMPATIBILITY DECISION
→ APPROVE | HOLD | REJECT
```

## Atualizações major

Nunca atualizar automaticamente versão major de framework agentic. Exige ADR ou decisão registrada equivalente, benchmark antes/depois e rollback.

## Atualizações minor/patch

Podem ser automatizadas apenas para descoberta/PR. Merge continua condicionado a CI e revisão. Patch de segurança pode receber prioridade, mas não dispensa teste de regressão proporcional ao risco.

## Evidência mínima

Registrar:

- framework e versão atual/nova;
- data/release;
- links oficiais;
- mudanças relevantes;
- advisories/issues conhecidos;
- dependências alteradas;
- testes executados;
- métricas antes/depois;
- riscos residuais;
- decisão e responsável.

## Benchmarks mínimos para frameworks de agente

- task success;
- correctness;
- latency;
- tokens/custo quando aplicável;
- tool call count;
- retry/error rate;
- state integrity;
- verified action rate;
- duplicate side-effect rate em cenários com ação;
- security violations em suíte controlada.

## Stop conditions

Bloquear adoção quando houver:

- regressão de segurança sem mitigação;
- alteração incompatível de approval semantics;
- perda de traceability;
- aumento de duplicate side effects;
- failure mode sem timeout/cancelamento;
- licença incompatível;
- dependência crítica vulnerável sem mitigação;
- resultado não reproduzível.

## Rollback

A versão anterior aprovada e lockfile/config correspondente devem permanecer recuperáveis até conclusão da janela de validação da nova versão.