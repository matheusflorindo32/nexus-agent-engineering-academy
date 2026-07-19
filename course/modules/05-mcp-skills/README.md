---
id: course.module.05-mcp-skills
title: 05 — MCP e Skills
lang: pt-BR
status: foundation
prerequisites: [course.module.04-loop-engineering]
---

# 05 — MCP e Skills

## Objetivos

- Explicar host, client, server, primitives, transport e capability negotiation do MCP.
- Projetar autorização sem token passthrough e com audience binding.
- Empacotar uma capacidade como skill delimitada e portável.

## Pré-requisitos

[Módulo 04](../04-loop-engineering/README.md); JSON-RPC, OAuth e processos locais.

## Progressão NEXUS

Conceito: interoperabilidade → arquitetura: host–client–server → implementação: recurso/tool mínimo → comparação: MCP,
função e plugin → projeto real: servidor read-only + skill operacional.

## Laboratórios

- LAB-501 — inspecionar negociação e falhar com versão/capacidade incompatível.

## Projeto

Servidor MCP mínimo com allowlist, entradas validadas, autorização adequada ao transporte e threat model.

## Checklist

- [ ] Fixei versão do protocolo e SDK.
- [ ] O host mantém consentimento e isolamento.
- [ ] Tokens são validados para o recurso correto.

## Bibliografia

FIELDING, Roy T. *Architectural Styles and the Design of Network-based Software Architectures*. 2000.

## Referências

[MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25), acesso 2026-07-19;
[RFC 8707](https://www.rfc-editor.org/rfc/rfc8707), 2020.

