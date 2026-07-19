---
id: course.module.11-automation
title: 11 — Automação agentic
lang: pt-BR
status: foundation
prerequisites: [course.module.10-observability-engineering]
---

# 11 — Automação agentic

## Objetivos

- Separar orquestração determinística de decisão probabilística.
- Projetar webhooks, filas, idempotency keys, compensação e approval tasks.
- Implementar o mesmo fluxo em código e automação visual e comparar trade-offs.
- Instrumentar cada etapa com telemetria, owner, SLA, retry budget e trilha de auditoria.

## Pré-requisitos

[Módulo 10 — Observability Engineering](../10-observability-engineering/README.md); APIs, eventos, filas, idempotência e padrões de integração.

## Progressão NEXUS

Conceito: automação confiável → arquitetura: event–workflow–agent–gate → implementação: workflow idempotente → comparação: SDK/n8n/Make → projeto real: processo com SLA, observabilidade e rollback.

## Laboratórios

- [LAB-1101 — Idempotência e compensação](../../../labs/LAB-1101-idempotent-automation.md): repetir, concorrer e recuperar eventos sem duplicar efeitos.

## Projeto

Automação que processa evento, usa agente apenas na decisão ambígua, exige aprovação, registra efeitos por chave idempotente e reconcilia o resultado após falha parcial.

## Checklist

- [ ] Reentrega e execução concorrente são seguras.
- [ ] Estado, ownership e correlação de cada etapa estão visíveis.
- [ ] Existe caminho manual quando IA ou dependência falha.
- [ ] Efeitos externos usam idempotency key e ledger verificável.
- [ ] Retry, timeout, compensação e dead-letter queue têm limites explícitos.
- [ ] Alertas possuem owner, runbook e condição de resolução.

## Critérios de excelência

- Reentrega, concorrência e falha parcial não duplicam efeitos.
- Compensação e reconciliação são demonstráveis e auditáveis.
- Telemetria permite reconstruir evento, decisão, aprovação e efeito.
- O workflow degrada com segurança sem ampliar privilégios.

## Bibliografia

HOHPE, Gregor; WOOLF, Bobby. *Enterprise Integration Patterns*. Addison-Wesley, 2003.

## Referências

- [CloudEvents 1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md), CNCF, 2022.
- [NIST SP 800-204D](https://doi.org/10.6028/NIST.SP.800-204D), estratégias de segurança para software baseado em eventos.
