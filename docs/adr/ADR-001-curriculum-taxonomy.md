---
id: adr.001.curriculum-taxonomy
title: ADR-001 — Taxonomia curricular e unicidade de numeração
lang: pt-BR
status: review
---

# ADR-001 — Taxonomia curricular e unicidade de numeração

## Status

Proposto para revisão humana no PR corretivo. Esta decisão só se torna aceita após merge explícito.

## Contexto

A auditoria do PR #5 confirmou colisões de numeração entre módulos e laboratórios. O validador anterior registrava prefixos em conjuntos, o que ocultava duplicidades. Também havia conflito entre `LAB-1001` de observabilidade e a reserva histórica de idempotência.

## Decisão

Adotar uma única trilha curricular canônica:

| Número | Módulo |
|---:|---|
| 00 | Orientação |
| 01 | Fundamentos |
| 02 | Context Engineering |
| 03 | Tool Engineering |
| 04 | Loop Engineering |
| 05 | Memory Engineering |
| 06 | Multi-Agent Systems |
| 07 | Evaluation Engineering |
| 08 | Guardrails e Security Engineering |
| 09 | Production Architecture |
| 10 | Observability Engineering |
| 11 | Automação agentic |
| 12 | Capstone production-grade |

Regras obrigatórias:

1. número, `id`, slug e diretório de módulo são únicos;
2. cada laboratório possui identificador único;
3. referências internas devem apontar apenas para a trilha canônica;
4. conteúdo legado removido da árvore ativa permanece rastreável no histórico Git e deve ser registrado no guia de migração;
5. novas especializações não podem reutilizar a numeração da trilha principal;
6. o validador deve falhar diante de colisões, lacunas obrigatórias ou pré-requisitos inexistentes.

## Laboratórios canônicos afetados

- `LAB-801`: security red team;
- `LAB-1001`: observabilidade agentic;
- `LAB-1101`: automação idempotente e compensável.

## Alternativas rejeitadas

### Manter dois módulos com o mesmo número

Rejeitada por quebrar navegação, pré-requisitos, rastreabilidade e automação de validação.

### Renumerar apenas o novo módulo

Rejeitada porque não resolveria as colisões históricas detectadas nos módulos 05–09 e no LAB-801.

### Enfraquecer o validador

Rejeitada porque converteria uma falha de contrato em falso negativo permanente.

## Consequências

### Positivas

- progressão curricular determinística;
- links e pré-requisitos verificáveis;
- numeração de laboratórios sem ambiguidade;
- CI capaz de bloquear regressões estruturais.

### Custos e riscos

- links externos ou materiais já publicados podem apontar para caminhos antigos;
- histórico de conteúdo precisa ser consultado durante migrações;
- futuras mudanças de taxonomia exigem ADR e guia de migração.

## Critérios de aceite

- Modules 00–12 presentes uma única vez;
- LABs obrigatórios presentes uma única vez;
- nenhum link interno quebrado;
- nenhum `id` duplicado;
- validador e workflows verdes no SHA final;
- guia de migração publicado.

## Evidência de teste

```bash
python tests/validate_repository.py
```

O teste deve reprovar fixtures com prefixos duplicados e aprovar a árvore canônica.

## Referências

Ver [Referências ABNT e rastreabilidade](../references/REFERENCIAS_ABNT.md).
