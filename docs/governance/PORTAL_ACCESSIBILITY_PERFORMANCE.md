---
id: governance.portal-accessibility-performance
title: Baseline de acessibilidade e performance do portal
lang: pt-BR
status: review
version: 0.1.0
---

# Baseline de acessibilidade e performance do portal

## Objetivo

Adicionar controles automatizados e auditáveis sobre o HTML estático candidato e sobre o tamanho do artefato, sem representar esses controles como auditoria completa de acessibilidade ou medição real de experiência.

## Hard gates

A execução falha quando qualquer página HTML não apresenta:

- idioma declarado no elemento `html`;
- título de documento;
- região principal de conteúdo;
- cabeçalho de nível 1;
- texto alternativo declarado em imagens;
- nome acessível mínimo em botões.

Também falha quando:

- o artefato completo excede 12 MiB;
- qualquer arquivo isolado excede 2 MiB;
- o relatório de evidências não é produzido.

## Evidências

O bundle contém `report.json` com páginas verificadas, achados, tamanho total do build, maior arquivo, falhas de orçamento e limitações.

## Interpretação

Um resultado verde sustenta apenas que os contratos estáticos e os orçamentos definidos foram satisfeitos nesta execução.

## Limitações

Este controle não substitui:

- axe-core ou Lighthouse;
- navegação por teclado;
- leitores de tela;
- contraste computado;
- testes com pessoas com deficiência;
- Core Web Vitals;
- métricas de usuários reais;
- testes em produção;
- auditoria WCAG independente.

CI verde não implica conformidade, aprovação, release ou merge. O protocolo permanece em `status: review` até validação técnica e humana.
