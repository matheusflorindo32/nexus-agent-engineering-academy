---
id: governance.next-milestone
title: Próximo Milestone — Runtime Security Convergence V1.1
lang: pt-BR
status: review
reviewed_at: 2026-08-26
---

# Próximo Milestone — Runtime Security Convergence V1.1

## Objetivo

Fechar as assimetrias que o Provider Runtime Trial V1 expôs antes de qualquer Provider/Model Trial externo ou expansão para novos frameworks.

## Prioridade P0

### Google ADK — A2A/HITL integrity
- executar pause/resume real;
- approval scoped;
- parallel tool calls;
- state/session restore;
- side effect sintético com receipt;
- retry sem duplicação;
- classificar issues upstream somente após reprodução.

### MCP — remote adversarial lab
- Streamable HTTP/transport atual;
- version negotiation;
- MRTR;
- cancellation;
- tool metadata poisoning;
- hostile tool output;
- OAuth issuer/audience/resource;
- DNS/host validation;
- credential passthrough;
- network interruption/recovery.

### Supply chain
- gerar lock/constraints transitivos;
- hashes quando suportados;
- SBOM/provenance quando tecnicamente viável;
- comparar ambiente resolvido com baseline;
- bloquear major/minor agentic upgrades sem gate.

### Observability
- esquema NEXUS para spans/events;
- OpenTelemetry por runtime quando disponível;
- redaction antes de export;
- provar ausência de secrets em artifacts/logs de teste.

## Prioridade P1

- criar cenário side-effect equivalente para ADK e host MCP;
- completar VAR/DSER de forma comparável;
- adicionar cancellation explícito onde o SDK oferecer contrato;
- testar state/memory integrity;
- ampliar failure injection de smoke para chaos matrix.

## Microsoft Agent Framework

Antes de Runtime Trial:
1. criar Contract Trial paritário;
2. registrar versão/risco/capabilities;
3. executar supply-chain review;
4. somente então decidir promoção a runtime.

Não adicionar MAF apenas para aumentar cobertura de frameworks.

## Provider/Model Trial

Continua bloqueado. Exige:
- autorização explícita;
- credenciais em secret store;
- orçamento;
- modelo/configuração fixos;
- dataset e prompts versionados;
- repetições pré-definidas;
- análise estatística;
- política de retenção de traces;
- critérios de exclusão antes dos dados.

## Definition of Done

- CI completa verde;
- A2A/HITL e MCP remoto possuem testes executados ou status NOT_EXECUTED justificado;
- supply chain mais forte que top-level pins;
- observability/redaction verificadas;
- claims atualizados com limites;
- revisão adversarial independente;
- novo PR aberto sem auto-merge.
