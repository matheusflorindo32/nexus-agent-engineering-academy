---
id: course.module.06-evaluation
title: 06 — Avaliação de agentes
lang: pt-BR
status: foundation
prerequisites: [course.module.05-mcp-skills]
---

# 06 — Avaliação de agentes

## Objetivos

- Construir datasets com casos normais, limites, ataques e abstention.
- Separar métricas de resultado, trajetória, segurança, custo e latência.
- Calibrar avaliação humana, determinística e model-based sem circularidade.

## Pré-requisitos

[Módulo 05](../05-mcp-skills/README.md); estatística descritiva e testes.

## Progressão NEXUS

Conceito: qualidade mensurável → arquitetura: dataset–runner–scorer–report → implementação: eval harness → comparação:
offline/online e judge/humano → projeto real: quality gate de release.

## Laboratórios

- LAB-601 — medir regressão com seed/corpus fixos e intervalos de incerteza.

## Projeto

Suíte reproduzível que compara baseline e agente, registra configuração e bloqueia regressão crítica de segurança.

## Checklist

- [ ] Dataset não é contaminado pelo desenvolvimento.
- [ ] Métrica tem definição e limiar justificado.
- [ ] Falhas são inspecionáveis, não apenas um score agregado.

## Bibliografia

JURAN, Joseph M.; GODFREY, A. Blanton. *Juran’s Quality Handbook*. McGraw-Hill, 1999.

## Referências

[NIST AI RMF 1.0](https://doi.org/10.6028/NIST.AI.100-1), 2023.

