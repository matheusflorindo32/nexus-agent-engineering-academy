---
id: project.capstone
title: Capstone production-grade
lang: pt-BR
status: foundation
---

# Capstone production-grade

## Brief

Resolva um processo real delimitado, com proprietário e usuários identificados, usando IA apenas onde incerteza exige.
O piloto deve operar em sandbox ou escopo reversível.

## Gates

1. **Discovery:** problema, baseline, dados e não objetivos aprovados.
2. **Architecture:** ADRs, C4, threat model, contratos e SLOs revisados.
3. **Vertical slice:** caminho ponta a ponta com fake tools e eval.
4. **Hardening:** least privilege, approval, observabilidade, rollback e game day.
5. **Defense:** demo, evidência, limites, custos e roadmap.

## Entregáveis

Código/workflow reproduzível, documentação operacional, dataset permitido, eval report, threat model, inventário de
dependências, SBOM quando aplicável, runbook e apresentação técnica.

## Rubrica

| Dimensão | Peso | Gate crítico |
|---|---:|---|
| Problema e evidência | 15% | baseline comparável |
| Arquitetura | 20% | contratos e decisões rastreáveis |
| Qualidade/eval | 20% | regressões críticas bloqueiam release |
| Segurança/privacidade | 25% | sem permissão excessiva ou segredo |
| Operação/SRE | 15% | pause, recovery e rollback demonstrados |
| Comunicação | 5% | reprodução por terceiro |

