---
id: course.module.09-multi-agent-systems
title: 09 — Sistemas multiagentes
lang: pt-BR
status: foundation
prerequisites: [course.module.08-security]
---

# 09 — Sistemas multiagentes

## Objetivos

- Justificar decomposição multiagente contra baseline single-agent.
- Projetar roteamento, handoff, identidade, estado compartilhado e resolução de conflito.
- Medir coordenação, amplificação de erro, custo e latência.

## Pré-requisitos

[Módulo 08](../08-security/README.md); sistemas distribuídos básicos.

## Progressão NEXUS

Conceito: coordenação especializada → arquitetura: router/graph/blackboard → implementação: dois especialistas →
comparação: topologias → projeto real: fluxo com escalonamento humano.

## Laboratórios

- LAB-901 — comparar single agent e router+specialists no mesmo corpus.

## Projeto

Sistema com contratos de handoff, isolamento de capacidade, trace causal e fallback single-agent.

## Checklist

- [ ] Há ganho medido que justifica complexidade.
- [ ] Agentes não podem autoampliar capacidade.
- [ ] Deadlock, livelock e mensagem duplicada foram testados.

## Critérios de excelência

- O ganho sobre o baseline single-agent é mensurável e os handoffs permanecem rastreáveis e limitados por capacidade.

## Bibliografia

WOOLDRIDGE, Michael. *An Introduction to MultiAgent Systems*. 2. ed. Wiley, 2009.

## Referências

[FIPA Specifications](http://www.fipa.org/repository/standardspecs.html), arquivo institucional, acesso 2026-07-19.

