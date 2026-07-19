---
id: course.module.03-tool-engineering
title: 03 — Tool Engineering
lang: pt-BR
status: foundation
prerequisites: [course.module.02-context-engineering]
---

# 03 — Tool Engineering

## Objetivos

- Escrever contratos de entrada/saída estreitos e validar parâmetros fora do modelo.
- Classificar efeitos, idempotência, autorização e estratégias de retry.
- Projetar preview, confirmação e reconciliação para ações externas.

## Pré-requisitos

[Módulo 02](../02-context-engineering/README.md); HTTP, JSON Schema e testes básicos.

## Progressão NEXUS

Conceito: tool como boundary → arquitetura: model–policy gate–adapter → implementação: tool read-only → comparação:
função local, API e MCP → projeto real: operação com dry-run e audit log.

## Laboratórios

- LAB-301 — endurecer uma ferramenta deliberadamente ampla e testar parâmetros hostis.

## Projeto

Criar uma tool idempotente com schema, autorização contextual, timeout, erro tipado e teste de duplicidade.

## Checklist

- [ ] O modelo não escolhe identidade, escopo ou credencial.
- [ ] Retry é proibido para efeito ambíguo não idempotente.
- [ ] Logs não contêm segredos.

## Bibliografia

NEWMAN, Sam. *Building Microservices*. 2. ed. O’Reilly, 2021.

## Referências

[JSON Schema 2020-12](https://json-schema.org/draft/2020-12), especificação, acesso 2026-07-19.

