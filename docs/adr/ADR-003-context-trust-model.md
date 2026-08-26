---
id: adr.003.context-trust-model
title: ADR-003 — Context Trust Model
lang: pt-BR
status: review
---

# ADR-003 — Context Trust Model

## Status

Proposto para revisão humana; efetivo após merge explícito.

## Contexto

Agentes recebem instruções, dados do usuário, documentos, memória, web, tool outputs e MCP metadata. Sem uma taxonomia explícita, conteúdo externo pode ser promovido implicitamente a instrução confiável.

## Decisão

Adotar níveis T0–T7:

- T0 system/immutable policy;
- T1 repository-controlled instructions;
- T2 approved Skills;
- T3 trusted tools;
- T4 user data;
- T5 external documents;
- T6 web/MCP/third-party content;
- T7 unknown/adversarial.

Conteúdo de nível inferior não pode ampliar permissões, reclassificar sua própria confiança ou substituir políticas de nível superior.

## Consequências

- provenance passa a ser dado de controle, não apenas metadata editorial;
- tool/MCP output deve ser rotulado e validado antes de influenciar ação;
- memória deve preservar origem/trust level;
- testes adversariais devem verificar não escalada.

## Alternativas rejeitadas

### Confiar apenas no prompt de sistema

Rejeitada: prompt injection indireta explora exatamente a mistura entre instrução e dados.

### Um único rótulo trusted/untrusted

Rejeitada por perder distinções úteis entre políticas, Skills aprovadas, tools e conteúdo externo.

## Critérios de aceite

- modelo documentado em threat model;
- helper determinístico de não escalada;
- teste `test_untrusted_mcp_instruction` em CI;
- adapters futuros registram origem/trust level quando relevante;
- nenhuma camada T5–T7 é promovida para T0–T2 apenas por texto do modelo.

## Risco residual

A taxonomia não classifica automaticamente conteúdo malicioso e não substitui autorização, sandboxing ou policy gates.