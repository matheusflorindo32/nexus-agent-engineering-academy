---
id: course.module.10-automation
title: 10 — Automação agentic
lang: pt-BR
status: foundation
prerequisites: [course.module.09-multi-agent-systems]
---

# 10 — Automação agentic

## Objetivos

- Separar orquestração determinística de decisão probabilística.
- Projetar webhooks, filas, idempotency keys, compensação e approval tasks.
- Implementar o mesmo fluxo em código e automação visual e comparar trade-offs.

## Pré-requisitos

[Módulo 09](../09-multi-agent-systems/README.md); APIs, eventos e filas.

## Progressão NEXUS

Conceito: automação confiável → arquitetura: event–workflow–agent–gate → implementação: workflow → comparação:
SDK/n8n/Make → projeto real: processo com SLA e rollback.

## Laboratórios

- LAB-1001 — repetir eventos e provar idempotência sem duplicar efeitos.

## Projeto

Automação que processa evento, usa agente apenas na decisão ambígua, exige aprovação e reconcilia o resultado.

## Checklist

- [ ] Reentrega e execução concorrente são seguras.
- [ ] Estado e ownership de cada etapa estão visíveis.
- [ ] Existe caminho manual quando IA/dependência falha.

## Critérios de excelência

- Reentrega, concorrência e falha parcial não duplicam efeitos, e o rollback permanece demonstrável.

## Bibliografia

HOHPE, Gregor; WOOLF, Bobby. *Enterprise Integration Patterns*. Addison-Wesley, 2003.

## Referências

[CloudEvents 1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md), CNCF, 2022.

