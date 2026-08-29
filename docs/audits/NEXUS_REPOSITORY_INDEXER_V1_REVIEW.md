---
id: audit.nexus-repository-indexer-v1-review
content_id: audit.nexus-repository-indexer-v1-review
version: 1.0.0
title: NEXUS Repository Indexer V1 — Review
lang: pt-BR
status: review
reviewed_at: 2026-08-28
---

# NEXUS Repository Indexer V1 — Review

## Architecture review

PASS dentro do boundary V1: o indexador é uma camada read-only abaixo do Control Plane e produz documento compatível com Traceability Graph V2. Não há graph database, SDK ou parser third-party.

## Security review

Controles executáveis cobrem path traversal, symlinks, vendor/generated directories, arquivos oversized, malformed Python, bounded file/symbol counts e conteúdo com marcadores de prompt injection. Repository content é parseado por `ast` e nunca executado. Network e repository writes permanecem zero por contrato e por evidência do trial.

Riscos residuais: parser Python stdlib ainda processa input potencialmente adversarial; limites reduzem DoS mas não constituem sandbox formal. Symlink TOCTOU em filesystem hostil não foi testado. Encoding além de UTF-8 é tratado como skip, não convertido.

## Adversarial review

Antes do indexador, o review automático do PR #59 encontrou dois defeitos no Graph V2: recursive DFS podia gerar `RecursionError` e propagava `CYCLE` para ancestrais fora do ciclo. Ambos foram reproduzidos em RED nesta branch e corrigidos com traversal iterativo que marca somente o segmento ativo da back-edge.

Para o indexador, casos adversariais incluem malformed AST, hostile comments, ignored generated/vendor paths, unsafe relative paths, symlinks e arquivos oversized. Conteúdo suspeito gera somente telemetria de texto não confiável; `instructions_executed` permanece zero.

## Traceability audit

O output V1 produz `file` e `symbol` nodes e `CONTAINS_SYMBOL`/`DEPENDS_ON`. A camada não cria requirement/spec/task/test/evidence por inferência; esses continuam sob autoridade do Control Plane. Integração completa ocorre quando esses nós são conectados pelos contratos Graph V2 existentes.

## Reproducibility audit

Protocolo e fixtures possuem SHA-256 congelados em `fixture-manifest.json`; o workflow verifica hashes antes do benchmark quando o manifest está `FROZEN`. Python 3.12 e Ubuntu 24.04 são explicitados no workflow. Cinco repetições são exigidas para fixtures.

## Independent verification boundary

CI real, workflow dedicado e Codex/GitHub review são evidências independentes da execução inline, mas não equivalem a auditoria humana externa. Human review e merge continuam gates separados.

## Technical debt

1. Python-only V1.
2. Resolução de imports é estática e conservadora; imports dinâmicos não são resolvidos.
3. Rename inference real via Git não implementada.
4. Índice incremental reutiliza hash/content record, mas não persiste cache entre jobs por padrão.
5. Ground truth completo do próprio repositório não existe; métricas de precision/recall são apenas das fixtures.
6. Teste de escala extrema além dos bounds não é benchmark de produção.
