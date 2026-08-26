---
id: adr.005.atomic-skill-updates
title: ADR-005 — Atomic Skill Updates
lang: pt-BR
status: review
---

# ADR-005 — Atomic Skill Updates

## Status

Proposto para revisão humana; efetivo após merge explícito.

## Contexto

Skills podem ser lidas por agentes enquanto outro processo atualiza seus arquivos. Reescrita in-place pode produzir estado parcial, `ENOENT` transitório ou conteúdo misto.

## Decisão

Adotar versões imutáveis com staging e promoção atômica quando suportada pelo filesystem:

`stage → validate → audit → hash → test → atomic promote → update current pointer → monitor`.

Nunca sobrescrever diretamente uma versão ativa.

## Requisitos

- diretório `.staging` isolado;
- `SKILL.md` validado antes da promoção;
- hash de conteúdo;
- versão imutável;
- ponteiro `current` atualizado atomicamente;
- versão anterior preservada para rollback;
- loader diferencia I/O transitório de conteúdo inválido.

## Alternativas rejeitadas

### Rewrite in-place

Rejeitada por expor leitores a arquivos ausentes/parciais.

### Apagar versão anterior após promoção

Rejeitada por impedir rollback imediato.

## Critérios de aceite

- reference registry com staging/hash/promotion;
- teste `test_skill_atomic_update`;
- teste `test_skill_integrity_hash`;
- documentação de limitações de atomicidade por filesystem;
- registry completo só será criado se necessário ao experimento.

## Risco residual

`os.replace` não é garantia de transação distribuída. NFS/object stores/registries remotos exigem mecanismos próprios de versionamento/compare-and-swap.