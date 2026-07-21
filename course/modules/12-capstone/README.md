---
id: course.module.12-capstone
title: 12 — Capstone production-grade
lang: pt-BR
status: foundation
prerequisites: [course.module.11-automation]
---

# 12 — Capstone production-grade

## Objetivos

- Integrar arquitetura, contexto, tools, loops, avaliação, observabilidade, automação e segurança.
- Defender decisões com evidência, ADRs e comparação multiplataforma.
- Operar um piloto controlado com rollback, game day e postmortem.

## Pré-requisitos

Módulos 00–11 concluídos e projeto aprovado no [brief do capstone](../../../projects/capstone/README.md).

## Progressão NEXUS

Conceito: sistema sociotécnico → arquitetura: C4 + threats + SLOs → implementação: vertical slice → comparação: adapter alternativo → projeto real: piloto controlado, game day e defesa técnica.

## Laboratórios

- `LAB-1201` está **planejado e ainda não foi implementado**. Seu escopo previsto é um game day no qual uma dependência falha, uma injeção aparece e o budget é consumido sem perda de rastreabilidade. Até sua publicação, esta descrição não constitui atividade disponível nem requisito de conclusão.

## Projeto

Entregar sistema executável, demo segura, eval report, threat model, runbook, ADRs, custos, limitações, evidências de observabilidade, automação idempotente e roadmap.

## Checklist

- [ ] Requisitos e não objetivos são rastreáveis.
- [ ] Eval e segurança bloqueiam release quando falham.
- [ ] Operador consegue observar, pausar, retomar e reverter.
- [ ] Outra pessoa reproduz a demo sem segredo compartilhado.
- [ ] Falhas parciais e duplicações são tratadas sem efeitos indevidos.
- [ ] Evidências pós-incidente permitem reconstrução causal.

## Critérios de excelência

- A entrega integra avaliação, segurança, operação, automação e rollback com evidência suficiente para reprodução independente.
- O sistema mantém invariantes de segurança e idempotência durante game day.
- Limitações, riscos residuais e decisões arquiteturais são explícitos.

## Bibliografia

FORD, Neal et al. *Software Architecture: The Hard Parts*. O’Reilly, 2021.

## Referências

- [NIST Secure Software Development Framework 1.1](https://doi.org/10.6028/NIST.SP.800-218), 2022.
- [Google SRE Workbook](https://sre.google/workbook/table-of-contents/), acesso 2026-07-19.
