---
id: platform.google-adk-python
title: Adapter experimental — Google ADK Python
lang: pt-BR
status: review
verified: 2026-08-26
---

# Adapter experimental — Google ADK Python

Fonte primária: documentação e releases oficiais de `google/adk-python`.

- Linha 2.x estável verificada: `2.7.1` (2026-08-17).
- Status NEXUS: `experimental-contract`.
- Execução real do SDK neste milestone: **não**.

## Capacidades verificadas

ADK 2.x declara workflow runtime com grafos, routing, fan-out/fan-in, loops, retry, state management, HITL e nested workflows. A Task API cobre delegação agent-to-agent; a linha 2.7.x inclui melhorias de correctness, task mode, eval persistence e tracing/tool metadata.

## Achado upstream relevante

A issue oficial `google/adk-python#6721`, aberta em 2026-08-14, descreve falha potencial de resume em um cenário A2A + human-input na 2.7.0. O NEXUS **não reproduziu** esse comportamento com o runtime Google porque o SDK não é executado neste milestone.

Classificação: `POTENTIALLY_APPLICABLE`.

Não chamar de vulnerabilidade NEXUS. Não chamar de advisory de segurança Google. Tratar como issue upstream aberta que justifica teste regressivo quando o adapter real for ativado.

## Contrato NEXUS

O adapter real deverá provar:

1. integridade `REQUESTED → APPROVED → EXECUTED → VERIFIED` em HITL;
2. resume correto após pausa/approval;
3. nenhum double side effect em retries ou parallel tool calls;
4. state/session integrity;
5. timeout, cancel e cleanup;
6. tracing sem exposição de payload sensível;
7. A2A/handoff com identidade e proveniência rastreáveis.

## Gate específico A2A/HITL

A ativação de side effects reais fica bloqueada até existir teste com versão pinada do ADK que cubra approval scoped, resume, receipt externo e reconciliação após retry.

O benchmark V3 atual mede apenas o contrato NEXUS determinístico, não o runtime ADK real.
