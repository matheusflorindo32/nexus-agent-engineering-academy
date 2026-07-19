---
id: course.module.04-loop-engineering
title: 04 — Loop Engineering
lang: pt-BR
status: foundation
prerequisites: [course.module.03-tool-engineering]
---

# 04 — Loop Engineering

## Objetivos

- Modelar o loop agentic como máquina de estados.
- Implementar budgets, stop conditions, checkpoint, retry e circuit breaker.
- Demonstrar terminação em cenários de sucesso, estagnação e falha.

## Pré-requisitos

[Módulo 03](../03-tool-engineering/README.md); máquinas de estado e exceções.

## Progressão NEXUS

Conceito: feedback controlado → arquitetura: estados/transições → implementação: loop determinístico → comparação:
loop em SDKs/grafos → projeto real: pesquisador interrompível.

## Laboratórios

- [LAB-401](../../../labs/LAB-401-stop-conditions.md) — provar stop conditions com falhas injetadas.

## Projeto

Loop retomável com budgets multidimensionais, detecção de no-progress e relatório de término tipado.

## Checklist

- [ ] Todo caminho alcança complete, await ou stopped.
- [ ] Checkpoint não duplica efeitos.
- [ ] Circuit breaker possui limiar, cooldown e probe.

## Bibliografia

NYGARD, Michael T. *Release It!*. 2. ed. Pragmatic Bookshelf, 2018.

## Referências

[AWS Builders’ Library — Timeouts, retries and backoff](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/), acesso 2026-07-19.

