---
id: adr.006.framework-upgrade-gate
title: ADR-006 — Framework Upgrade Gate
lang: pt-BR
status: review
---

# ADR-006 — Framework Upgrade Gate

## Status

Proposto para revisão humana; efetivo após merge explícito.

## Contexto

Frameworks de agentes podem mudar silenciosamente semântica de handoff, tool calling, HITL, state, tracing e retries. Atualização sem benchmark pode introduzir regressões operacionais ou de segurança.

## Decisão

Toda versão nova relevante passa por:

`release review → issue/security review → sandbox branch → regression → benchmark → security benchmark → approve/hold/reject`.

Versões major nunca são auto-merged.

## Critérios de decisão

Bloquear adoção se houver regressão sem mitigação em:

- approval semantics;
- state integrity;
- duplicate side effects;
- timeout/cancellation;
- observability;
- security boundaries;
- license/dependency risk.

## Evidência exigida

Registrar versões, release notes, fontes oficiais, testes, métricas antes/depois, riscos residuais e rollback.

## Alternativas rejeitadas

### Atualizar sempre para latest

Rejeitada porque novidade não implica melhoria e frameworks agentic têm superfícies de regressão não capturadas por semver sozinho.

### Fixar indefinidamente

Rejeitada porque impede correções de segurança e evolução controlada.

## Critérios de aceite

- política publicada;
- radar atualizado;
- future adapters usam versão registrada;
- CI/benchmark gate disponível antes da primeira atualização relevante.

## Risco residual

Issues desconhecidos podem existir mesmo após gate. Monitoramento upstream continua necessário.