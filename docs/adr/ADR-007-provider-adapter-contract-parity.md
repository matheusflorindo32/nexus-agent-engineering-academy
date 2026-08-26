---
id: adr.007.provider-adapter-contract-parity
title: ADR-007 — Paridade de contrato antes de benchmark de runtime
lang: pt-BR
status: review
---

# ADR-007 — Paridade de contrato antes de benchmark de runtime

## Contexto

Comparar OpenAI Agents SDK, Google ADK e MCP diretamente com exemplos diferentes produziria resultados não defensáveis. Além disso, instalar três stacks novas antes de definir contratos comuns aumentaria superfície de supply chain, custos e ambiguidade de causalidade.

## Decisão

Adotar duas fases obrigatórias:

1. **Contract Trial** — wrappers/declarations stdlib-only exercitam os mesmos invariantes NEXUS: VAR, RSR, DSER e CTVR, sem provider calls.
2. **Runtime Trial** — cada tecnologia é executada com versão pinada, ambiente reproduzível, mesma tarefa/dataset/model constraints, tracing e chaos scenarios.

Resultados de Contract Trial nunca serão apresentados como benchmark do framework real.

## Contrato mínimo comum

- timeout/cancellation bounded;
- terminal failure observável;
- approval scoped;
- `APPROVED != EXECUTED != VERIFIED`;
- `operation_id` e receipt em side effects;
- retry/reconciliation sem double effect;
- conteúdo externo sem escalada de trust;
- provenance/version registradas;
- métricas machine-readable.

## Consequências

### Positivas

- reduz claims falsos de equivalência;
- separa falha do NEXUS de falha do framework;
- permite CI gratuito e determinístico;
- cria oracle comum para adapters reais.

### Custos

- não produz ainda números de latência/custo/tokens dos frameworks;
- exige um segundo milestone com dependências e providers reais.

## Alternativas rejeitadas

### Instalar tudo e benchmarkar imediatamente

Rejeitada por confundir diferenças de setup, modelo, rede e SDK com diferenças arquiteturais.

### Usar apenas documentação comparativa

Rejeitada porque não cria regressão executável.

## Gate de promoção

Um adapter só pode ir de `TRIAL — contract only` para `TRIAL — runtime` após: pin de versão, dependency/supply-chain review, ambiente reproduzível, testes negativos, observabilidade e rollback.
