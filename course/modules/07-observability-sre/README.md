---
id: course.module.07-observability-sre
title: 07 — Observabilidade e SRE para agentes
lang: pt-BR
status: foundation
prerequisites: [course.module.06-evaluation]
---

# 07 — Observabilidade e SRE para agentes

## Objetivos

- Definir SLI/SLO para qualidade, segurança, latência, custo e disponibilidade.
- Correlacionar execução, chamadas de modelo, ferramentas e efeitos externos.
- Projetar telemetry redaction, retenção, alertas e runbooks.

## Pré-requisitos

[Módulo 06](../06-evaluation/README.md); logs, métricas e tracing.

## Progressão NEXUS

Conceito: operabilidade → arquitetura: sinais + correlação → implementação: trace estruturado → comparação: logs,
métricas e spans → projeto real: dashboard e runbook.

## Laboratórios

- LAB-701 — diagnosticar latência/custo anormal a partir de traces sanitizados.

## Projeto

Definir SLOs e alertas acionáveis, demonstrando investigação e mitigação de um incidente simulado.

## Checklist

- [ ] Cada efeito possui correlation ID e actor.
- [ ] Prompts/outputs sensíveis não vazam por padrão.
- [ ] Alertas apontam para runbooks testados.

## Critérios de excelência

- Sinais, alertas e runbooks permitem diagnosticar e mitigar o incidente simulado sem expor dados sensíveis.

## Bibliografia

BEYER, Betsy et al. *Site Reliability Engineering*. O’Reilly, 2016.

## Referências

[OpenTelemetry Specification](https://opentelemetry.io/docs/specs/), acesso 2026-07-19.

