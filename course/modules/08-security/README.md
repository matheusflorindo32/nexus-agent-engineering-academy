---
id: course.module.08-security
title: 08 — Segurança de sistemas agentes
lang: pt-BR
status: foundation
prerequisites: [course.module.07-observability-sre]
---

# 08 — Segurança de sistemas agentes

## Objetivos

- Produzir threat model de fronteiras agentic e MCP.
- Implementar least privilege, approval gates, secret handling e egress control.
- Executar testes adversariais e responder a incidente simulado.

## Pré-requisitos

[Módulo 07](../07-observability-sre/README.md) e [baseline de segurança](../../../docs/security/index.md).

## Progressão NEXUS

Conceito: zero trust para contexto/ações → arquitetura: policy enforcement → implementação: gates determinísticos →
comparação: mitigação por prompt e por sistema → projeto real: hardening + incident drill.

## Laboratórios

- LAB-801 — prompt injection indireta em corpus controlado, sem acesso a sistemas reais.

## Projeto

Endurecer um agente vulnerável, documentar risco residual e demonstrar containment, rotation e recovery.

## Checklist

- [ ] Nenhum controle depende apenas de o modelo “obedecer”.
- [ ] Aprovações incluem alvo, efeito e expiração.
- [ ] O playbook preserva evidência e reconcilia efeitos.

## Critérios de excelência

- O hardening bloqueia os casos adversariais definidos, preserva evidência e documenta o risco residual.

## Bibliografia

ANDERSON, Ross. *Security Engineering*. 3. ed. Wiley, 2020.

## Referências

[OWASP AI Agent Security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html), acesso 2026-07-19;
[NIST AI 600-1](https://doi.org/10.6028/NIST.AI.600-1), 2024.

