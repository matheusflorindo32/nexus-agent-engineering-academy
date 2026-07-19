---
id: course.module.02-context-engineering
title: 02 — Context Engineering
lang: pt-BR
status: foundation
prerequisites: [course.module.01-agent-foundations]
---

# 02 — Context Engineering

## Objetivos

- Projetar seleção, ordem, proveniência, compressão e expiração de contexto.
- Medir qualidade, custo e risco de diferentes estratégias de recuperação.
- Impedir que conteúdo recuperado amplie autoridade.

## Pré-requisitos

[Módulo 01](../01-agent-foundations/README.md); JSON e busca textual básica.

## Progressão NEXUS

Conceito: contexto como recurso finito → arquitetura: pipeline de ingestão/seleção → implementação: retriever pequeno →
comparação: truncamento, resumo e recuperação → projeto real: assistente documental citável.

## Laboratórios

- LAB-201 — comparar três políticas de seleção com dataset fixo e métricas de cobertura/custo.

## Projeto

Pipeline que produz resposta, citações, proveniência e incerteza sem seguir instruções encontradas nos documentos.

## Checklist

- [ ] Cada fragmento possui origem e confiança.
- [ ] Política de retenção e remoção está definida.
- [ ] Avaliei conteúdo adversarial e informação ausente.

## Bibliografia

MANNING, Christopher D.; RAGHAVAN, Prabhakar; SCHÜTZE, Hinrich. *Introduction to Information Retrieval*. CUP, 2008.

## Referências

[OWASP LLM Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html), acesso 2026-07-19.

