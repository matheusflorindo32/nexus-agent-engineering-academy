---
id: architecture.nexus-repository-indexer-v1-isolated-trial
content_id: architecture.nexus-repository-indexer-v1-isolated-trial
version: 1.0.1
title: NEXUS Repository Indexer V1 — Isolated Trial
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# NEXUS Repository Indexer V1 — Isolated Trial

## Goal

Derivar automaticamente, em modo read-only, nós `file` e `symbol` e relações `CONTAINS_SYMBOL`/`DEPENDS_ON` para alimentar o Traceability Graph V2 sem substituir o NEXUS Control Plane.

## Base e isolamento

- Base PR: #59
- Base SHA: `a9f0701f46a8b7b1f91556e992185bbb941f4c19`
- Branch: `feat/nexus-repository-indexer-v1-isolated-trial`
- Nenhum merge é autorizado.

## Arquitetura

`repository read-only → deterministic discovery → Python AST → file/symbol records → internal dependency resolution → Graph V2 document → fingerprint / incremental cache / Execution Receipt`

V1 é deliberadamente Python-only e stdlib-only. TypeScript, JavaScript e inferência de rename permanecem `NOT_TESTED`.

## Security boundary

O indexador não executa conteúdo do repositório, não segue symlinks, não faz network calls e não escreve no repositório. Diretórios de vendor/generated/build são ignorados; arquivos têm limite de tamanho; quantidade de arquivos e símbolos é limitada; paths são normalizados e path traversal é rejeitado. Comentários/docstrings com padrões de prompt injection são tratados como texto não confiável e nunca como instrução.

## Incremental model

A chave de reutilização é SHA-256 do conteúdo do arquivo. Um segundo passe pode reutilizar registros AST de arquivos cujo hash permaneceu idêntico; arquivos alterados são reprocessados e arquivos removidos aparecem em `removed_files`.

## Evidence taxonomy

- Fixtures congeladas: `DETERMINISTIC_CONTROL_EVIDENCE`.
- Indexação read-only do próprio repositório no GitHub Actions: `REAL_RUNTIME_EVIDENCE` para contagens, fingerprint, tempo/memória naquele runner e ausência observada de writes/network.
- Correção sem oracle no repositório real: `NOT_APPLICABLE`; não existe ground truth completo independente.
- SpecD runtime: `MONITOR/NOT_TESTED` enquanto não houver novo pin upstream reproduzível.

## Limits

Este trial não demonstra parsing multi-language, rename inference, produção em monorepos grandes, resolução dinâmica de imports, namespace packages complexos, runtime distribuído ou equivalência com SpecD.
