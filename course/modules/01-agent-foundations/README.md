---
id: course.module.01-agent-foundations
title: 01 — Fundamentos de Agent Engineering
lang: pt-BR
status: foundation
prerequisites: [course.module.00-orientation]
---

# 01 — Fundamentos de Agent Engineering

## Objetivos

- Diferenciar modelo, assistente, workflow e agente usando critérios testáveis.
- Especificar objetivo, estado, ferramentas, política, budgets e saída.
- Identificar quando um fluxo determinístico é superior a um agente.

## Pré-requisitos

[Módulo 00](../00-orientation/README.md) e noções de APIs.

## Progressão NEXUS

Conceito: autonomia limitada → arquitetura: contrato de agente → implementação: agente read-only mínimo → comparação:
workflow determinístico versus agentic → projeto real: triagem com abstention.

## Laboratórios

- [LAB-101](../../../labs/LAB-101-agent-contract.md) — transformar pedido ambíguo em agent spec.

## Projeto

Projetar um agente de triagem sem escrita externa, com baseline não agentic e critérios de recusa.

## Checklist

- [ ] Objetivo e não objetivos são observáveis.
- [ ] Permissões e stop conditions estão explícitas.
- [ ] Existe baseline mais simples para comparação.

## Bibliografia

RUSSELL, Stuart; NORVIG, Peter. *Artificial Intelligence: A Modern Approach*. 4. ed. Pearson, 2020.

## Referências

[OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), docs oficiais, acesso 2026-07-19.

